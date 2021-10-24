from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "slug",
            "created",
            "modified",
        ]
        model = Workspace


class WorkspacesFilter(filters.FilterSet):
    class Meta:
        fields = {
            "slug": ["exact", "in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = Workspace


class WorkspacesViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    filterset_class = WorkspacesFilter

