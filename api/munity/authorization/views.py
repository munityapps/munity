from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets

from .models import Permission, Role

#################################################
# Permission
#################################################


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "ressource",
            "action",
        ]
        model = Permission


class PermissionsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "ressource": [
                "exact",
                "in",
            ],
            "action": [
                "exact",
                "in",
            ],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = Permission


class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_class = PermissionsFilter


#################################################
# Role
#################################################


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "permissions"]
        model = Role


class RolesFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "name": [
                "exact",
                "in",
            ],
            "permissions": ["exact", "in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = Role


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filterset_class = RolesFilter
