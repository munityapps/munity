from django_filters import rest_framework as filters
from ..files.views import FileSerializer
from rest_framework import serializers
from django.db.models.query_utils import Q
from .models import User, UserRoleWorkspace
from rest_framework.exceptions import PermissionDenied

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
            "has_overmind_access",
            "modified",
            "generic_groups",
            "user_role_workspaces",
            "password",
            "phone_number"
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

            # add new rights
            user_new_workspaces = []
            for user_role_workspace_data in user_role_workspaces_data:
                workspace = user_role_workspace_data.get("workspace")
                user_new_workspaces.append(workspace)
                UserRoleWorkspace.objects.filter(user=instance).filter(workspace=workspace).delete()
                UserRoleWorkspace.objects.update_or_create(
                    user=instance, **user_role_workspace_data
                )

            # remove revoked rights
            UserRoleWorkspace.objects.filter(user=instance).exclude(workspace__in=user_new_workspaces).delete()

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

class UsersViewSet(MunityViewSet):
    serializer_class = UserSerializer
    filterset_class = UsersFilter

    def destroy(self, request, pk=None, workspace_pk=None):
        # we suppose that user as permission USER DELETE for current workspace
        # but we need to perform some sanity check
        if not request.user.is_superuser:
            accessible_workspaces = UserRoleWorkspace.objects.filter(user=self.request.user)
            workspace_slugs = []
            for accessible_workspace in accessible_workspaces:
                workspace_slugs.append(accessible_workspace.workspace)
            user_to_delete = self.serializer_class.Meta.model.objects.filter(
                id=pk,
                user_role_workspaces__in=UserRoleWorkspace.objects.filter(workspace__in=workspace_slugs)
            ).first()
            if not user_to_delete:
                raise PermissionDenied({"message":"You cannot remove user, you don't have any workspace in common"})
        response = super().destroy(request, pk=pk , workspace_pk=workspace_pk)
        return response

    def create(self, request, workspace_pk=None):
        # we suppose that user as permission USER CREATE for current workspace
        # but we need to perform some sanity check
        if not request.user.is_superuser:
            if request.data.get('is_superuser'):
                raise PermissionDenied({"message":"You cannot create superuser"})

            accessible_workspaces = UserRoleWorkspace.objects.filter(user=self.request.user)
            workspace_slugs = []
            for accessible_workspace in accessible_workspaces:
                workspace_slugs.append(accessible_workspace.workspace.slug)
            user_role_workspaces = request.data.get('user_role_workspaces')
            if not user_role_workspaces:
                raise PermissionDenied({"message":"Cannot create user without roles"})
            for user_role_workspace in user_role_workspaces:
                if user_role_workspace.get('workspace') not in workspace_slugs:
                    raise PermissionDenied({"message":"You don't have permission to add user on this workspace"})
        response = super().create(request, workspace_pk)

        return response

    def update(self, request, workspace_pk=None, pk=None, partial=False):
        # we suppose that user as permission USER UPDATE for current workspace
        # but we need to perform some sanity check
        if not request.user.is_superuser:
            if request.data.get('is_superuser'):
                raise PermissionDenied({"message":"You cannot grant superuser privilege"})

            edited_user = self.get_queryset().filter(pk=pk).first()
            if edited_user is None:
                raise PermissionDenied({"message":"You cannot see this user"})

            if edited_user.is_superuser:
                raise PermissionDenied({"message":"You cannot edit superuser"})

            # update role if needed
            if 'user_role_workspaces' in request.data:
                accessible_workspaces = UserRoleWorkspace.objects.filter(user=self.request.user)
                workspace_slugs = []
                for accessible_workspace in accessible_workspaces:
                    workspace_slugs.append(accessible_workspace.workspace.slug)

                user_role_workspaces = request.data.get('user_role_workspaces')
                for user_role_workspace in user_role_workspaces:
                    if user_role_workspace.get('workspace') not in workspace_slugs:
                        raise PermissionDenied({"message":"You don't have permission to change this access"})

        response = super().update(request, pk=pk, workspace_pk=workspace_pk, partial=partial)
        return response

    # since user access workspaces by role, we have to adapt access permission through role and not workpace FK
    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(id=self.request.user.id) | Q(user_role_workspaces__workspace=self.kwargs["workspace_pk"])).distinct()
        # WE ARE ON OVERMIND!
        else:
            # super user see all overmind users
            if self.request.user.is_superuser:
                # return model.objects.filter(Q(is_superuser=True) | Q(has_overmind_access=True))
                return model.objects.all()
            # staff see user from his workspaces
            if self.request.user.has_overmind_access:
                # getting accessible workspaces
                accessible_workspaces = UserRoleWorkspace.objects.filter(user=self.request.user)
                workspace_slugs = []
                for accessible_workspace in accessible_workspaces:
                    workspace_slugs.append(accessible_workspace.workspace)
                # get all related roles
                return model.objects.filter(
                    user_role_workspaces__in=UserRoleWorkspace.objects.filter(workspace__in=workspace_slugs)
                )
            # users see nothing
            return None
