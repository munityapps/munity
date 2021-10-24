from django_filters import rest_framework as filters
from ..models import MunityGroupableModel
from munity.views import MunityWorkspaceViewSet
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "workspace",
            "username",
            "email",
            "roles",
            "first_name",
            "last_name",
            "created",
            "is_superuser",
            "modified",
            "generic_groups",
        ]
        model = User

class UsersFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "workspace": ["exact", "in"],
            "first_name": ["exact", "in", "contains"],
            "generic_groups": ["in"],
            "last_name": ["exact", "in", "contains"],
            "email": ["exact", "in", "contains"],
            "username": ["exact", "in", "contains"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = User


class UsersViewSet(MunityWorkspaceViewSet, MunityGroupableModel):
    serializer_class = UserSerializer
    filterset_class = UsersFilter

