from itertools import product

from django.core.management.base import BaseCommand

from acl.models import (
    GroupACL,
    GroupAction,
    GroupResource,
    GroupRole,
    WorkspaceACL,
    WorkspaceAction,
    WorkspaceResource,
    WorkspaceRole,
)
from dynamic_db_router import in_database
from munity.settings_acl import (
    ALL_GROUP_RESOURCES,
    ALL_WORKSPACE_RESOURCES,
    READ_AND_UPDATE_WORKSPACE_RESOURCES,
    USER_WORKSPACE_RESOURCES,
    DefaultGroupActionChoice,
    DefaultGroupRoleChoice,
    DefaultWorkspaceActionChoice,
    DefaultWorkspaceRoleChoice,
)
from settings.models import Settings

def _init_db():
    """
    Configures default ACL's:
        - Creates default WorkspaceRoles and GroupRoles
        - Creates default CRUD WorkspaceActions and GroupActions
        - Indexes WorkspaceResources on the basis of ContentType
        - Designates what resources are GroupResources
        - Fills the WorkspaceACL and GroupACL tables by associating roles, actions, and resources.
        - Populate initial Workspace settings
    """

    WorkspaceRole.objects.exclude(workspace_role_name__in=[el.value for el in DefaultWorkspaceRoleChoice]).delete()
    GroupRole.objects.exclude(group_role_name__in=[el.value for el in DefaultGroupRoleChoice]).delete()

    WorkspaceAction.objects.exclude(
        workspace_action_name__in=[el.value for el in DefaultWorkspaceActionChoice]
    ).delete()
    GroupAction.objects.exclude(group_action_name__in=[el.value for el in DefaultGroupActionChoice]).delete()

    WorkspaceResource.objects.exclude(
        workspace_resource_name__in=[
            workspace_resource_class.__name__ for workspace_resource_class in ALL_WORKSPACE_RESOURCES
        ]
    ).delete()
    GroupResource.objects.exclude(
        group_resource_name__in=[group_resource_class.__name__ for group_resource_class in ALL_GROUP_RESOURCES]
    ).delete()

    GroupACL.objects.all().delete()
    WorkspaceACL.objects.all().delete()

    # Create Workspace Roles and Group Roles
    w_role_Owner, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.OWNER.value)
    w_role_Admin, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.ADMIN.value)
    w_role_User, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.USER.value)

    g_role_Admin, __ = GroupRole.objects.get_or_create(group_role_name=DefaultGroupRoleChoice.ADMIN.value)
    g_role_User, __ = GroupRole.objects.get_or_create(group_role_name=DefaultGroupRoleChoice.USER.value)

    # Create Workspace Actions and Group Actions
    w_action_CREATE, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.CREATE.value
    )
    w_action_READ, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.READ.value
    )
    w_action_UPDATE, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.UPDATE.value
    )
    w_action_DELETE, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.DELETE.value
    )
    w_action_ADD_TO_GROUP, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.ADD_TO_GROUP.value
    )
    w_action_REMOVE_FROM_GROUP, __ = WorkspaceAction.objects.get_or_create(
        workspace_action_name=DefaultWorkspaceActionChoice.REMOVE_FROM_GROUP.value
    )

    # g_action_CREATE, __ = GroupAction.objects.get_or_create(group_action_name=DefaultGroupActionChoice.CREATE.value)
    g_action_READ, __ = GroupAction.objects.get_or_create(group_action_name=DefaultGroupActionChoice.READ.value)
    g_action_UPDATE, __ = GroupAction.objects.get_or_create(group_action_name=DefaultGroupActionChoice.UPDATE.value)
    g_action_ADD_TO_GROUP, __ = GroupAction.objects.get_or_create(
        group_action_name=DefaultGroupActionChoice.ADD_TO_GROUP.value
    )
    g_action_REMOVE_FROM_GROUP, __ = GroupAction.objects.get_or_create(
        group_action_name=DefaultGroupActionChoice.REMOVE_FROM_GROUP.value
    )

    workspace_actions = [
        w_action_CREATE,
        w_action_READ,
        w_action_UPDATE,
        w_action_DELETE,
        w_action_ADD_TO_GROUP,
        w_action_REMOVE_FROM_GROUP,
    ]
    workspace_actions_read_or_update = [w_action_READ, w_action_UPDATE]
    group_actions = [g_action_READ, g_action_UPDATE, g_action_ADD_TO_GROUP, g_action_REMOVE_FROM_GROUP]
    group_actions_no_add_or_remove = [g_action_READ, g_action_UPDATE]  # NOQA: F841

    # Create Workspace Resources and Group Resources
    all_workspace_resources = [
        WorkspaceResource.objects.get_or_create(workspace_resource_name=workspace_resource_class.__name__)[0]
        for workspace_resource_class in ALL_WORKSPACE_RESOURCES
    ]

    user_workspace_resources = [
        WorkspaceResource.objects.get_or_create(workspace_resource_name=workspace_resource_class.__name__)[0]
        for workspace_resource_class in USER_WORKSPACE_RESOURCES
    ]

    read_and_update_workspace_resources = [
        WorkspaceResource.objects.get_or_create(workspace_resource_name=workspace_resource_class.__name__)[0]
        for workspace_resource_class in READ_AND_UPDATE_WORKSPACE_RESOURCES
    ]

    all_group_resources = [
        GroupResource.objects.get_or_create(group_resource_name=group_resource_class.__name__)[0]
        for group_resource_class in ALL_GROUP_RESOURCES
    ]

    # Workspace ACLs ------------------------------------------------------------------------------------
    # Create all ACL to give every right on ALL_WORKSPACE_RESOURCES to the Workspace Owner.
    # Workspace Admins have every right on ALL_WORKSPACE_RESOURCES.
    # The difference from Owner is that Admins can be Deleted, whereas Owners cannot.
    for role, action, resource in product([w_role_Owner, w_role_Admin], workspace_actions, all_workspace_resources):
        __, __ = WorkspaceACL.objects.get_or_create(
            workspace_role=role, workspace_action=action, workspace_resource=resource
        )

    # Workspace Users only have READ rights on USER_WORKSPACE_RESOURCES
    for role, action, resource in product([w_role_User], [w_action_READ], user_workspace_resources):
        __, __ = WorkspaceACL.objects.get_or_create(
            workspace_role=role, workspace_action=action, workspace_resource=resource
        )

    # People from all WorkspaceRoles have Workspace-level READ & UPDATE rights on READ_AND_UPDATE_WORKSPACE_RESOURCES
    for role, action, resource in product(
        WorkspaceRole.objects.all(), workspace_actions_read_or_update, read_and_update_workspace_resources
    ):
        __, __ = WorkspaceACL.objects.get_or_create(
            workspace_role=role, workspace_action=action, workspace_resource=resource
        )

    # Group ACLs ------------------------------------------------------------------------------------

    # Group Admins can READ & UPDATE + ADD & REMVOE on ALL_GROUP_RESOURCES within the Group
    for role, action, resource in product([g_role_Admin], group_actions, all_group_resources):
        __, __ = GroupACL.objects.get_or_create(group_role=role, group_action=action, group_resource=resource)

    # Group Users can only READ ON on ALL_GROUP_RESOURCES within the Group
    for role, action, resource in product([g_role_User], [g_action_READ], all_group_resources):
        __, __ = GroupACL.objects.get_or_create(group_role=role, group_action=action, group_resource=resource)

    # Remove ACL entries for operations that are forbidden for everyone
    WorkspaceACL.objects.filter(
        workspace_action__workspace_action_name__in=["CREATE", "UPDATE"],
        workspace_resource__workspace_resource_name="AlertNotification",
    ).delete()
    GroupACL.objects.filter(
        group_action__group_action_name__in=["CREATE", "UPDATE"],
        group_resource__group_resource_name="AlertNotification",
    ).delete()

    # Workspace settings
    Settings.objects.all().delete()

class Command(BaseCommand):
    help = "Initializes a database with default ACL's."

    def add_arguments(self, parser):
        parser.add_argument("--workspace_slug", default="default", type=str, help='Specify a custom workspace')

    def handle(self, *args, **options):
        workspace_slug = options.get("workspace_slug")
        with in_database(workspace_slug, write=True):
            _init_db()

        self.stdout.write(self.style.SUCCESS(f'Successfully initialized the "{workspace_slug}" database.'))
