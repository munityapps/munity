from functools import partial
from django_filters import rest_framework as filters
from ..files.views import FileSerializer
from rest_framework import serializers, viewsets
from django.db.models.query_utils import Q
from .models import User, UserRoleWorkspace
from ..models import MunityGroupableModel
from ..workspaces.models import Workspace
from django.contrib.contenttypes.models import ContentType

from ..utils import UUIDEncoder
from ..records.models import Record
from deepdiff import DeepDiff
import json

from ..views import MunityViewSet


class UserRoleWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('workspace', 'role')
        model = UserRoleWorkspace

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "created",
            "avatar",
            "is_superuser",
            "modified",
            "generic_groups",
            "user_role_workspaces",
            "password",
        ]
        model = User
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    password=serializers.CharField(required=False)
    user_role_workspaces = UserRoleWorkspaceSerializer(many=True)

    # We show full avatar in formation on get, on update we only use doc id
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['avatar'] = FileSerializer(instance.avatar).data if instance.avatar else None
        return response

    def update(self, instance, validated_data):
        if 'user_role_workspaces' in validated_data:
            user_role_workspaces_data = validated_data.pop('user_role_workspaces')

            user_workspaces = []
            for user_role_workspace_data in user_role_workspaces_data:
                user_workspaces.append(user_role_workspace_data.get("workspace"))
                UserRoleWorkspace.objects.update_or_create(
                    user=instance, **user_role_workspace_data
                )
            # remove removed rights
            UserRoleWorkspace.objects.filter(user=instance).exclude(workspace__in=user_workspaces).delete()

        user = super(self.__class__, self).update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user

    def create(self, validated_data):
        user_role_workspaces_data = validated_data.pop('user_role_workspaces')
        user = User.objects.create(**validated_data)
        for user_role_workspace_data in user_role_workspaces_data:
            UserRoleWorkspace.objects.create(
                user=user, **user_role_workspace_data
            )
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user


class UsersFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "first_name": ["exact", "in", "contains"],
            "generic_groups": ["in"],
            "last_name": ["exact", "in", "contains"],
            "email": ["exact", "in", "contains"],
            "username": ["exact", "in", "contains"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = User

class UsersViewSet(MunityViewSet, MunityGroupableModel):
    serializer_class = UserSerializer
    filterset_class = UsersFilter

    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(id=self.request.user.id) | Q(user_role_workspaces__workspace=self.kwargs["workspace_pk"]))
        return model.objects.filter(is_superuser=True)

