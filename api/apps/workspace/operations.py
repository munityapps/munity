import datetime
import subprocess
import time
import traceback

from django.apps import apps
from django.conf import settings
from django.db import connection, connections
from dynamic_db_router import in_database

import jwt
from accounts.models import User
from acl.models import WorkspaceRole
from outputs.emails import ConfirmAccountEmail
from outputs.models import Log
from munity.settings_acl import DefaultWorkspaceRoleChoice
from slugify import slugify
from workspace.exceptions import CreateDatabaseError, DatabaseAlreadyExistsError
from workspace.existing_workspaces import ExistingWorkspace
from workspace.models import WorkspaceSettings
from groups.models import Group

from .signals import workspace_created_signal


def list_existing_workspaces():
    """CAUTION: This returns workspace_db_names, not workspace_slugs."""

    return ExistingWorkspace(
        db_user=settings.DATABASES["default"]["USER"],
        db_host=settings.DATABASES["default"]["HOST"],
        db_password=settings.DATABASES["default"]["PASSWORD"],
    ).list_existing_workspaces()


def delete_workspace(workspace_slug):
    workspace_db_name = "workspace_" + workspace_slug.replace("-", "_")
    connection.close()
    try:
        # Execute PostgreSQL commands to safely drop the database
        out = subprocess.check_output(  # NOQA: F841
            f"""psql "host={settings.DATABASES['default']['HOST']} """
            f"""dbname=postgres """
            f"""port={settings.DATABASES['default']['PORT']} """
            f"""user={settings.DATABASES['default']['USER']} """
            f"""password={settings.DATABASES['default']['PASSWORD']}" """
            f'''-c "'''
            f"""SELECT pg_terminate_backend(pg_stat_activity.pid) """
            f"""FROM pg_stat_activity """
            f"""WHERE pg_stat_activity.datname = '{workspace_db_name}' """
            f'''  AND pid <> pg_backend_pid();"''',
            shell=True,
        )
        out2 = subprocess.check_output(  # NOQA: F841
            f"""psql "host={settings.DATABASES['default']['HOST']} """
            f"""dbname=postgres """
            f"""port={settings.DATABASES['default']['PORT']} """
            f"""user={settings.DATABASES['default']['USER']} """
            f"""password={settings.DATABASES['default']['PASSWORD']}" """
            f'''-c "DROP DATABASE {workspace_db_name};"''',
            shell=True,
        )
        traceback.print_exc()
        print(f"Dropped Database {workspace_db_name}")
    except:  # NOQA: E722
        traceback.print_exc()

def create_workspace(
    owner_email, owner_password, workspace_name, owner_firstname, owner_lastname, lang="en", owner_social_id=""
):
    """Creates a workspace and an owner associated to it.
    i.e. creates a database named workspace_db_name, and creates an owner inside it.
    NB: owner_password must be in clear.
    """

    # workspace_name : Munity Platform
    # workspace_slug : munity-platform
    # workspace_db_name : workspace_munity_platform
    workspace_slug = slugify(workspace_name.strip())
    workspace_db_name = "workspace_" + workspace_slug.replace("-", "_")

    # Check whether the DB already exists. If positive, raise an exception
    existing_workspaces = list_existing_workspaces()
    if workspace_db_name in existing_workspaces:
        raise DatabaseAlreadyExistsError(workspace_name)

    # Connect to the postgresql server and creates a database named workspace_db_name
    try:
        # Kill all remaining connections to database reference (or we cannot dupplicate it).
        out = subprocess.check_output(
            f"""psql "host={settings.DATABASES['default']['HOST']} """
            f"""port={settings.DATABASES['default']['PORT']} """
            f"""dbname=postgres """
            f"""user={settings.DATABASES['default']['USER']} """
            f"""password={settings.DATABASES['default']['PASSWORD']}" """
            f"""-c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'reference' AND pid <> pg_backend_pid();" """,
            shell=True,
        )
        # This is safe from SQL and Command Injections since workspace_db_name is slugified a few lines above
        out = subprocess.check_output(
            f"""psql "host={settings.DATABASES['default']['HOST']} """
            f"""port={settings.DATABASES['default']['PORT']} """
            f"""dbname=postgres """
            f"""user={settings.DATABASES['default']['USER']} """
            f"""password={settings.DATABASES['default']['PASSWORD']}" """
            f"""-c "CREATE DATABASE {workspace_db_name} """
            f'''TEMPLATE {settings.DATABASES['default']['NAME']};"''',
            shell=True,
        )
        # os_command_console_output = str(out.decode('utf8').strip())
    except subprocess.CalledProcessError:
        # Command returns a non-zero exit code
        raise CreateDatabaseError()

    try:
        # Dynamically create a django connection to the newly created workspace database
        workspace_credentials = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": workspace_db_name,
            "USER": settings.DATABASES["default"]["USER"],
            "PASSWORD": settings.DATABASES["default"]["PASSWORD"],
            "HOST": settings.DATABASES["default"]["HOST"],
            "PORT": settings.DATABASES["default"]["PORT"],
        }
        connections.databases[workspace_slug] = workspace_credentials

        with in_database(workspace_slug, write=True):
            # Create the Owner inside the newly created database
            owner_workspace_role, __ = WorkspaceRole.objects.get_or_create(
                workspace_role_name=DefaultWorkspaceRoleChoice.OWNER.value
            )

            # Using the create_user function, django automatically salts and hashes the password
            # with the pbkdf2_sha256 algorithm.
            user_activation_state = False
            if settings.DEFAULT_USER_ACCOUNT_STATUS:
                user_activation_state = True

            owner = User.objects.create_superuser(
                username=owner_email,
                email=owner_email,
                password=owner_password,
                workspace_role=owner_workspace_role,
                first_name=owner_firstname,
                last_name=owner_lastname,
                is_active=user_activation_state,
                social_id=owner_social_id,
            )

            # Define the workspace_name in WorkspaceSettings
            WorkspaceSettings.objects.update_or_create(
                key="workspace_name", defaults={"value": workspace_name}
            )

            # Log Activities
            log = Log(
                username=owner_email,
                user_id=str(owner.id),
                action_type="CREATE (Workspace)",
                modified_model_name="WorkspaceSettings",
                modified_object_name=workspace_name,
                modified_object_id=str(
                    WorkspaceSettings.objects.get(key="workspace_name").workspace_setting_id
                ),
                role_name=owner_workspace_role.workspace_role_name,
                workspace_name=workspace_name,
            )
            log.save()

            workspace_created_signal.send(sender=type(workspace_slug), workspace_slug=workspace_slug)

    except:  # NOQA: E722
        delete_workspace(workspace_slug)
        raise

    send_account_activation(owner, workspace_slug, lang)

    return workspace_slug


def send_account_activation(owner, workspace_slug, lang):
    """
    Creates a token and send by mail for comfirm account.
    """
    exp = time.mktime(
        (
            datetime.datetime.today() + datetime.timedelta(minutes=settings.ACCOUNT_VALIDATION_KEY_EXPIRATION_MINUTES)
        ).timetuple()
    )

    data = {"workspace": workspace_slug, "email": owner.email, "exp": exp, "lang": lang}

    email_params = {
        "user": owner.first_name,
        "domain": "https://" + workspace_slug + ".app." + settings.DOMAIN_NAME,
        "token": jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode("utf-8"),
    }
    email_factory = ConfirmAccountEmail(email_params)
    email = email_factory.create_email_msg([owner.email], lang=lang, from_email=settings.SUPPORT_MAIL)
    email.send()
    return True


def get_workspace_setting_value(workspace_slug, key):
    """Retrieves the value of a workspace setting."""
    return WorkspaceSettings.objects.using(workspace_slug).get(key=key).value


def get_workspace_name_from_slug(workspace_slug):
    return get_workspace_setting_value(workspace_slug, "workspace_name")
