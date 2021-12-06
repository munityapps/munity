from django.db.models.query_utils import Q
from munity.authorization.models import Permission
from munity.users.models import UserRoleWorkspace
from rest_framework import permissions

from ..utils import get_request_info

class HasEndpointPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_active:
            return False

        # \o\ Super admin has god power /o/
        if request.user.is_superuser:
            return True

        (workspace_slug, ressource, action) = get_request_info(request)

        # We can get list even on overmind, we are limitted from our roles
        if action == 'list':
            return True
        # User with workspace privilege can invite/delete/update user for their workspaces
        if request.user.has_overmind_access and ressource == 'users':
            return True

        # searching for needed permission
        needed_permission = Permission.objects.filter(
            action=action,
            ressource__app_label=ressource
        )

        # we can self edit (view will check for right permission on admin actions)
        if ressource == 'users' and action == 'update':
            if request.data.get("id") == str(request.user.id):
                # wtf try to become admin oO
                if request.data.get("is_superadmin"):
                    return False
                # wtf try to get ownership
                if request.data.get("has_overmind_access"):
                    return False
                # remove role changement for self edition
                del request.data["user_role_workspaces"]
                return True

        # All user can manage files
        if ressource == 'files':
            return True

        # checking if user as at least one role that fit needed permission on wanted workspace or on all workspace
        has_role_permission = UserRoleWorkspace.objects.filter(
            Q(user=request.user) &
            Q(Q(workspace=workspace_slug) | Q(workspace=None)) &
            Q(role__permissions__in=needed_permission)
        )

        return has_role_permission