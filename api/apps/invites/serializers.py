from acl.serializers import GroupRoleSerializer, WorkspaceRoleSerializer
from base.serializers import ModelSerializerWithFields
from groups.serializers import GroupSerializer
from invites.models import Invite, InviteGroupMembership
from rest_framework import serializers


class InviteGroupMembershipSerializer(ModelSerializerWithFields):
    class Meta:
        model = InviteGroupMembership
        exclude = ("invite",)

    group = GroupSerializer(read_only=True, required=False, fields=("id", "name"))
    invite_id = serializers.UUIDField(write_only=True)
    group_id = serializers.UUIDField(write_only=True)
    group_role = GroupRoleSerializer(read_only=True, required=False)
    group_role_id = serializers.UUIDField(write_only=True)


class InviteSerializer(ModelSerializerWithFields):
    """
   Lists the Invites and their ACL's.
   UPDATE can be used to change a Invite's workspace_role_id
   """

    class Meta:
        model = Invite
        fields = "__all__"

    email = serializers.CharField(required=False)
    invite_group_memberships = InviteGroupMembershipSerializer(read_only=True, many=True)
    workspace_role = WorkspaceRoleSerializer(read_only=True, required=False)
    workspace_role_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
