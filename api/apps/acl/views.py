from acl.models import (GroupACL, GroupAction, GroupResource, GroupRole, WorkspaceACL, WorkspaceAction,
                        WorkspaceResource, WorkspaceRole)
from acl.serializers import (GroupACLSerializer, GroupActionSerializer, GroupResourceSerializer, GroupRoleSerializer,
                             WorkspaceACLSerializer, WorkspaceActionSerializer, WorkspaceResourceSerializer,
                             WorkspaceRoleSerializer)
from base.decorators import workspace_specific
from base.viewsets import MultipleDBModelViewSet


class GroupRoleViewSet(MultipleDBModelViewSet):
    serializer_class = GroupRoleSerializer
    queryset = GroupRole.objects.none()

    @workspace_specific
    def get_queryset(self):
        return GroupRole.objects.all()


class GroupActionViewSet(MultipleDBModelViewSet):
    serializer_class = GroupActionSerializer
    queryset = GroupAction.objects.none()

    @workspace_specific
    def get_queryset(self):
        return GroupAction.objects.all()


class GroupResourceViewSet(MultipleDBModelViewSet):
    serializer_class = GroupResourceSerializer
    queryset = GroupResource.objects.none()

    @workspace_specific
    def get_queryset(self):
        return GroupResource.objects.all()


class GroupACLViewSet(MultipleDBModelViewSet):
    serializer_class = GroupACLSerializer
    queryset = GroupACL.objects.none()

    @workspace_specific
    def get_queryset(self):
        return GroupACL.objects.all().select_related()


class WorkspaceRoleViewSet(MultipleDBModelViewSet):
    serializer_class = WorkspaceRoleSerializer
    queryset = WorkspaceRole.objects.none()

    @workspace_specific
    def get_queryset(self):
        return WorkspaceRole.objects.all()


class WorkspaceActionViewSet(MultipleDBModelViewSet):
    serializer_class = WorkspaceActionSerializer
    queryset = WorkspaceAction.objects.none()

    @workspace_specific
    def get_queryset(self):
        return WorkspaceAction.objects.all()


class WorkspaceResourceViewSet(MultipleDBModelViewSet):
    serializer_class = WorkspaceResourceSerializer
    queryset = WorkspaceResource.objects.none()

    @workspace_specific
    def get_queryset(self):
        return WorkspaceResource.objects.all()


class WorkspaceACLViewSet(MultipleDBModelViewSet):
    serializer_class = WorkspaceACLSerializer
    queryset = WorkspaceACL.objects.none()

    @workspace_specific
    def get_queryset(self):
        return WorkspaceACL.objects.all().select_related()
