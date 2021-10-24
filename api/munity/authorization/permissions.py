from django.db.models.query_utils import Q
from munity.authorization.models import Permission
from munity.users.models import UserRoleWorkspace
from rest_framework import permissions

from ..utils import get_request_info

class HasEndpointPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        (workspace_slug, ressource, action) = get_request_info(request)
        # searching for needed permission
        needed_permission = Permission.objects.filter(
            action=action,
            ressource__app_label=ressource
        )

        # checking if user as at least one role that fit needed permission on wanted workspace or on all workspace
        has_role_permission = UserRoleWorkspace.objects.filter(
            Q(user=request.user) &
            Q(Q(workspace=workspace_slug) | Q(workspace=None)) &
            Q(role__permissions__in=needed_permission)
        )

        return has_role_permission