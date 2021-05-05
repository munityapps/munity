import copy

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator

from accounts.models import User, UserGroupMembership
from accounts.serializers import UserGroupMembershipSerializer, UserSerializer
from acl.operations import has_workspace_permission, permission_required
from base.viewsets import MultipleDBModelViewSet
from groups.models import Group
from groups.serializers import GroupSerializer
from invites.models import Invite, InviteGroupMembership
from invites.serializers import InviteGroupMembershipSerializer, InviteSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from groups.operations import add_remove_groups, add_remove_devices, add_remove_users


class GroupViewSet(MultipleDBModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.none()

    def get_queryset(self):
        """
        This would be where we would restrict visibility to a subset of all groups in function of the user
        who makes the request.
        """
        if has_workspace_permission(self.request.user, self.action, self.queryset.model.__name__, self.request):
            return Group.objects.prefetch_related("groups").all()
        else:
            return Group.objects.prefetch_related("groups").filter(group_memberships__user=self.request.user).distinct()

    def list(self, request, page=None, step=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if step == None:
            step = settings.PAGE_SIZE
        count = len(serializer.data)
        if page is not None:
            # Pagination
            paginator = Paginator(serializer.data, step)
            try:
                return Response(data={"count": count, "results": list(paginator.get_page(page))})
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                return Response(data=[])

        return Response(data={"count": count, "groups": serializer.data})

    @permission_required
    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)

        group_created_id = result.data["id"]
        if group_created_id:
            group_created = Group.objects.get(id=group_created_id)

            ids = request.data.get("ids")
            ids = request.data.get("ids")
            users = request.data.get("users")

            add_remove_devices(group_created, ids)
            add_remove_groups(group_created, ids)
            add_remove_users(group_created, users)

            group_created = Group.objects.get(id=group_created_id)
            serializer = self.get_serializer(group_created, many=False)
            result = Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return result

    @permission_required
    def update(self, request, pk=None, *args, **kwargs):
        group = self.get_object()

        ids = request.data.get("ids")
        ids = request.data.get("ids")
        users = request.data.get("users")

        add_remove_devices(group, ids)
        add_remove_groups(group, ids)
        add_remove_users(group, users)

        return super().update(request, *args, pk=pk, **kwargs)

    @permission_required
    def bulk_destroy(self, request, *args, pk=None, **kwargs):
        ids = request.data.get("ids")

        if ids:
            if settings.INACTIVE_GROUP:
                inactive_group_uuid = settings.INACTIVE_GROUP_UUID
                if inactive_group_uuid:
                    group_inactive_exist = Group.objects.filter(
                        pk=inactive_group_uuid, name=settings.INACTIVE_GROUP_NAME
                    ).count()
                    if group_inactive_exist:
                        if inactive_group_uuid in ids:
                            ids.remove(inactive_group_uuid)

            groups = Group.objects.filter(pk__in=ids)
            nb_groups_deleted = len(groups)
            self.perform_bulk_destroy(groups)
            response = Response(data={"nb_groups_deleted": nb_groups_deleted})
        else:
            response = Response(status=status.HTTP_400_BAD_REQUEST)

        return response


class UserGroupMembershipViewSet(MultipleDBModelViewSet):
    serializer_class = UserGroupMembershipSerializer
    queryset = UserGroupMembership.objects.none()

    def get_queryset(self):  # FIXME user_id ?
        return UserGroupMembership.objects.all()

    @permission_required
    def list(self, request, user_id):
        queryset = UserGroupMembership.objects.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @permission_required
    def create(self, request, user_id):
        request_data = copy.deepcopy(request.data)
        if isinstance(request_data, dict):
            serializer = self.get_serializer(data={"user_id": user_id, **request_data})
        elif isinstance(request_data, list):
            serializer = self.get_serializer(
                data=[{"user_id": user_id, **membership_to_create_data} for membership_to_create_data in request_data],
                many=True,
            )
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_required
    def update(self, request, user_id, pk=None, partial=False):
        class ModifiedRequest:
            def __init__(self):
                self.data = copy.deepcopy(request.data)
                self.data["user_id"] = user_id
                self.META = request.META
                self.user = request.user

        if partial:
            return super().update(ModifiedRequest(), pk=pk, partial=True, user_id=user_id)
        else:
            return super().update(ModifiedRequest(), pk=pk, user_id=user_id)

    @permission_required
    def bulk_update(self, request, pk=None, partial=False, *args, **kwargs):
        out = []
        for element in request.data:
            for id in element.get("ids"):
                # if group membership object with these exact details does not exist, we create it
                if UserGroupMembership.objects.filter(user_id=element.get("user_id"), id=id).count() < 1:
                    UserGroupMembership.objects.create(
                        user_id=element.get("user_id"), id=id, group_role_id=element.get("group_role_id")
                    )
                # if has group but not same role, we update the role
                # elif (
                #    UserGroupMembership.objects.filter(
                #        user_id=element.get("user_id"), id=id, group_role_id=element.get("group_role_id")
                #    ).count()
                #    < 1
                # ):
                #    UserGroupMembership.objects.filter(user_id=element.get("user_id"), id=id).update(
                #        group_role_id=element.get("group_role_id")
                #    ),
                else:
                    # if the exact combination exists, it is removed
                    UserGroupMembership.objects.filter(user_id=element.get("user_id"), id=id).delete()
            out.append(UserSerializer(User.objects.filter(pk=element.get("user_id")).all()[0]).data)
        return Response(data=out)

    @permission_required
    def destroy(self, request, user_id, pk=None):

        return super().destroy(request, pk=pk)


class InviteGroupMembershipViewSet(MultipleDBModelViewSet):
    serializer_class = InviteGroupMembershipSerializer
    queryset = InviteGroupMembership.objects.none()

    def get_queryset(self):
        return InviteGroupMembership.objects.all()

    # @permission_required
    def list(self, request, invite_id):
        queryset = InviteGroupMembership.objects.filter(invite_id=invite_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @permission_required
    def create(self, request, invite_id):
        request_data = copy.deepcopy(request.data)
        if isinstance(request_data, dict):
            serializer = self.get_serializer(data={"invite_id": invite_id, **request_data})
        elif isinstance(request_data, list):
            serializer = self.get_serializer(
                data=[
                    {"invite_id": invite_id, **membership_to_create_data} for membership_to_create_data in request_data
                ],
                many=True,
            )
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except Exception as e:
            return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @permission_required
    def update(self, request, invite_id, pk=None, partial=False):
        class ModifiedRequest:
            def __init__(self):
                self.data = copy.deepcopy(request.data)
                self.data["invite_id"] = invite_id
                self.META = request.META
                self.invite = request.invite

        if partial:
            return super().update(ModifiedRequest(), pk=pk, partial=True, invite_id=invite_id)
        else:
            return super().update(ModifiedRequest(), pk=pk, invite_id=invite_id)

    @permission_required
    def bulk_update(self, request, pk=None, partial=False, *args, **kwargs):
        out = []
        for element in request.data:
            for id in element.get("ids"):
                # if group membership object with these exact details does not exist, we create it
                if (
                    InviteGroupMembership.objects.filter(invite_id=element.get("invite_id"), id=id).count()
                    < 1
                ):
                    InviteGroupMembership.objects.create(
                        invite_id=element.get("invite_id"),
                        id=id,
                        group_role_id=element.get("group_role_id"),
                    )
                else:
                    # if the exact combination exists, it is removed
                    InviteGroupMembership.objects.filter(invite_id=element.get("invite_id"), id=id).delete()
                out.append(InviteSerializer(Invite.objects.filter(pk=element.get("invite_id")).all()[0]).data)
        return Response(data=out)

    # @permission_required
    def destroy(self, request, invite_id, pk=None):
        return super().destroy(request, pk=pk)


@api_view(["GET"])
def group_summary(request, id, page):
    from outputs.models import Log

    # Get log list associated with device
    logs = (
        Log.objects.filter(modified_object_id=id)
        .order_by("-created_at")
        .values(
            "username",
            "action_type",
            "modified_model_name",
            "modified_object_name",
            "name",
            "role_name",
            "workspace_name",
            "created_at",
            "modification",
            "modified_object_id",
            "user_id",
        )
    )
    # Pagination
    paginator = Paginator(logs, settings.PAGE_SIZE)
    try:
        out_logs = list(paginator.get_page(page))
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return Response(data=[])
    count = logs.count()
    return Response(data={"count": count, "summary": out_logs})
