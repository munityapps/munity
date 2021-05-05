import importlib
import ast

from django.conf import settings

from accounts.reverse_lookup import RedisUserWorkspaceReverseLookup
from base import helpers
from base.viewsets import NoDestroyMixin
from outputs.emails import RetrieveWorkspaceEmail
from outputs.logs import get_logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import BulkModelViewSet
from slugify import slugify
from workspace import operations
from workspace.models import WorkspaceSettings
from workspace.operations import list_existing_workspaces
from workspace.serializers import WorkspaceSettingsSerializer

# Select the right populate_db command according to settings.FLAVOR
populate_db_command_name = "populate_db"
# + (
#     f"_{settings.FLAVOR.lower()}" if settings.FLAVOR.lower() != "default" else ""
# )
populate_db_command = importlib.import_module(f"project.management.commands.{populate_db_command_name}")


class WorkspaceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if settings.USE_SECURITY_CODE and request.data["security_code"] != settings.SECURITY_CODE:
            return Response('invalid_security_code', status=403)

        try:
            # Call perform_create_workspace with the request data
            lang = helpers._get_request_lang(request)
            workspace_slug = operations.create_workspace(
                owner_email=str(request.data["username"]).strip(),
                owner_password=str(request.data["password"]),
                workspace_name=str(request.data["workspace_name"]).strip(),
                owner_firstname=str(request.data["firstname"]).strip(),
                owner_lastname=str(request.data["lastname"]).strip(),
                lang=str(lang).strip(),
            )
        except Exception as e:  # Catches any exception, including those defined in exceptions.py
            error = {"exception": {"type": str(e.__class__.__name__), "name": str(e), "args": e.args}}
            log = get_logger(slugify(request.data["workspace_name"]).strip())
            log.error(
                "Failed initialization of workspace %s with error: %s",
                str(request.data["workspace_name"]).strip(),
                error,
            )
            return Response(error, status=getattr(e, "http_status_code", 500))
        else:
            # The operation is successful
            log = get_logger(workspace_slug)
            log.info("New workspace successfully created: %s", str(request.data["workspace_name"]).strip())
            return Response({"workspace_slug": workspace_slug})

    def delete(self, request, *args, **kwargs):
        """Delete a workspace and its entire database (cannot be undone). Only Owners can delete a workspace."""
        if request.user.workspace_role.workspace_role_name == "Owner":
            operations.delete_workspace(request.workspace_slug)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("only_the_workspace_owner_can_delete_the_workspace.")


@api_view(["POST"])
def check_security_code(request):
    security_code = request.data.get("security_code")

    if settings.USE_SECURITY_CODE and security_code != settings.SECURITY_CODE:
        response = Response("invalid_security_code", status=403)
    elif settings.USE_SECURITY_CODE and security_code == settings.SECURITY_CODE:
        response = Response({"security_code": security_code}, status=200)
    elif not settings.USE_SECURITY_CODE:
        response = Response(status=200)

    return response


@api_view(["POST"])
def check_exists(request):
    """
    Check if workspace exist.
    Return {"data": True} if workspace exists
    Return {"data": False} if workspace does not exist

    Usage example:
    requests.post(
        url='http://api.{{host}}/workspace/check-exist/',
        headers={'content-type': 'application/json'},
        data=json.dumps({
            'workspace': {{workspace}},
        })
    )
    """
    workspace_name = request.data.get("workspace")

    if not workspace_name:
        return Response({"message": "missing_workspace"})
    workspace_slug = slugify(workspace_name.strip())
    workspace_db_name = "workspace_" + workspace_slug.replace("-", "_")
    existing_workspaces = list_existing_workspaces()
    if workspace_db_name in existing_workspaces:
        return Response(status=400)
    return Response(
        {
            "workspace_name": workspace_name,
            "workspace_slug": workspace_slug,
        }
    )


@api_view(["POST"])
def recover_my_workspaces(request):
    """
        usage exemple:
        POST: http://api.{{host}}/workspace/recover
        body: {
            email: "john.doe@iot-valley.fr"
        }
    """
    lang = helpers._get_request_lang(request)
    workspace_slugs = RedisUserWorkspaceReverseLookup().get_workspaces_for_user(request.data.get("email", None))
    existing_workspaces = list_existing_workspaces()
    existing_workspaces = [existing_workspace.replace("workspace_", "") for existing_workspace in existing_workspaces]
    # remove previously deleted workspaces
    workspace_slugs = [
        workspace_slug for workspace_slug in workspace_slugs if workspace_slug.replace("-", "_") in existing_workspaces
    ]

    if len(workspace_slugs) == 0:
        return Response({"message": "no_workspace_found_for_user"}, status=status.HTTP_404_NOT_FOUND)

    workspace_slugs_and_names = {
        workspace_slug: operations.get_workspace_name_from_slug(workspace_slug) for workspace_slug in workspace_slugs
    }

    email_params = {
        "user": request.data["email"].split("@")[0],
        "header_url": "https://",
        "domain_url": settings.DOMAIN_NAME,
        "workspaces": workspace_slugs_and_names,
    }

    email_factory = RetrieveWorkspaceEmail(email_params)
    email = email_factory.create_email_msg(
        [request.data.get("email", None)], lang=lang, from_email=settings.SUPPORT_MAIL
    )
    email.send()
    if settings.DEBUG:
        email_params["workspaces"] = workspace_slugs
        return Response({"data": email_params})
    else:
        return Response()


def get_literal_eval(value):
    try:
        value = ast.literal_eval(value)
    except:
        pass
    return value


class WorkspaceSettingsViewSet(NoDestroyMixin, BulkModelViewSet):
    serializer_class = WorkspaceSettingsSerializer
    queryset = WorkspaceSettings.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            key = list(request.data.keys())[0]
            workspace_settings = WorkspaceSettings.objects.create(key=key, value=str(request.data.get(key)))
        except Exception as e:
            raise e

        if workspace_settings:
            serializer = self.get_serializer(workspace_settings)
            value = get_literal_eval(serializer.data.get("value"))

            return Response({serializer.data.get("key"): value}, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):

        queryset = self.get_queryset()
        ws = {}
        # ugly hotfix to add default value for this workspace settings
        ws['toast_success_color'] = '#24AB68'
        ws['toast_error_color'] = '#ED7474'
        ws['max_displayable_users'] = '3'
        for row in queryset:
            value = get_literal_eval(row.value)
            ws[row.key] = value
        return Response(ws)

    def update(self, request, pk=None):

        try:
            key = list(request.data.keys())[0]
            workspace_settings, created = WorkspaceSettings.objects.get_or_create(key=key)
        except:
            workspace_settings = None

        data = {"value": str(request.data.get(key))}
        serializer = self.get_serializer(workspace_settings, data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        value = get_literal_eval(serializer.data.get("value"))

        return Response({serializer.data.get("key"): value})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)
