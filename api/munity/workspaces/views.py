from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from ..users.models import UserRoleWorkspace
from rest_framework.exceptions import PermissionDenied


from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "slug",
            "name",
            "db_connection",
            "created",
            "modified",
        ]
        model = Workspace


class WorkspacesFilter(filters.FilterSet):
    class Meta:
        fields = {
            "slug": ["exact", "in"],
            "name": ["exact", "in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = Workspace

class WorkspacesViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceSerializer
    filterset_class = WorkspacesFilter

    # since user access workspaces by role, we have to adapt access permission through role and not workpace FK
    def get_queryset(self):
        model = self.serializer_class.Meta.model
        # super user see all
        if self.request.user.is_superuser:
            return model.objects.all()
        # users see only there workspaces
        accessible_workspaces = UserRoleWorkspace.objects.filter(user=self.request.user)
        workspace_slugs = []
        for accessible_workspace in accessible_workspaces:
            workspace_slugs.append(accessible_workspace.workspace)
        return model.objects.filter(slug__in=workspace_slugs)

