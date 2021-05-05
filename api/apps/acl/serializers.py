from acl.models import (GroupACL, GroupAction, GroupResource, GroupRole, WorkspaceACL, WorkspaceAction,
                        WorkspaceResource, WorkspaceRole)
from base.serializers import ModelSerializerWithFields
from rest_framework import serializers


class WorkspaceRoleSerializer(ModelSerializerWithFields):
    class Meta:
        model = WorkspaceRole
        exclude = ["created_at", "updated_at"]


class WorkspaceActionSerializer(ModelSerializerWithFields):
    class Meta:
        model = WorkspaceAction
        exclude = ["created_at", "updated_at"]


class WorkspaceResourceSerializer(ModelSerializerWithFields):
    class Meta:
        model = WorkspaceResource
        exclude = ["created_at", "updated_at"]


class WorkspaceACLSerializer(ModelSerializerWithFields):
    class Meta:
        model = WorkspaceACL
        exclude = ["created_at", "updated_at"]

    workspace_role = WorkspaceRoleSerializer(read_only=True)
    workspace_action = WorkspaceActionSerializer(read_only=True)
    workspace_resource = WorkspaceResourceSerializer(read_only=True)
    workspace_role_id = serializers.UUIDField(write_only=True)
    workspace_action_id = serializers.UUIDField(write_only=True)
    workspace_resource_id = serializers.UUIDField(write_only=True)


class GroupRoleSerializer(ModelSerializerWithFields):
    class Meta:
        model = GroupRole
        exclude = ["created_at", "updated_at"]

class GroupActionSerializer(ModelSerializerWithFields):
    class Meta:
        model = GroupAction
        exclude = ["created_at", "updated_at"]


class GroupResourceSerializer(ModelSerializerWithFields):
    class Meta:
        model = GroupResource
        exclude = ["created_at", "updated_at"]


class GroupACLSerializer(ModelSerializerWithFields):
    class Meta:
        model = GroupACL
        exclude = ["created_at", "updated_at"]

    group_role = GroupRoleSerializer(read_only=True)
    group_action = GroupActionSerializer(read_only=True)
    group_resource = GroupResourceSerializer(read_only=True)
    group_role_id = serializers.UUIDField(write_only=True)
    group_action_id = serializers.UUIDField(write_only=True)
    group_resource_id = serializers.UUIDField(write_only=True)
