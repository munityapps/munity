from .models import User, UserGroupMembership
from acl.models import WorkspaceRole
from acl.serializers import GroupRoleSerializer, WorkspaceRoleSerializer
from base.serializers import ModelSerializerWithFields
from groups.serializers import GroupSerializer
from rest_framework import serializers
from munity.settings_acl import DefaultWorkspaceRoleChoice


class UserGroupMembershipSerializer(ModelSerializerWithFields):
    class Meta:
        model = UserGroupMembership
        exclude = ("user", "created_at", "updated_at")

    group = GroupSerializer(read_only=True, required=False, fields=("id", "name", "custom_field"))
    user_id = serializers.UUIDField(write_only=True)
    id = serializers.UUIDField(write_only=True)
    group_role = GroupRoleSerializer(read_only=True, required=False)
    group_role_id = serializers.UUIDField(write_only=True)


class UserSerializer(ModelSerializerWithFields):
    """
    Lists the Users and their ACL's.
    UPDATE can be used to change a User's workspace_role_id
    """

    class Meta:
        model = User
        exclude = ["is_superuser", "is_staff", "is_active", "password", "groups"]

    username = serializers.CharField(required=False)
    group_memberships = serializers.SerializerMethodField()
    workspace_role = WorkspaceRoleSerializer(read_only=True, required=False)
    workspace_role_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    def validate_workspace_role_id(self, value):
        workspace_slug = self.context["request"].workspace_slug
        if WorkspaceRole.objects.using(workspace_slug).filter(pk=value).exists():
            return value

    def get_group_memberships(self, user):
        request = self.context.get("request", None)
        user_group_memberships = user.group_memberships
        if request:
            if request.user.workspace_role.workspace_role_name != DefaultWorkspaceRoleChoice.OWNER.value:
                user_id = request.user.id
                groups = user.get_associated_groups(user_id)
                user_group_memberships = user_group_memberships.filter(group__in=groups)

        serializer = UserGroupMembershipSerializer(user_group_memberships, many=True)
        return serializer.data
