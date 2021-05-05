import copy
import json

from accounts.operations import generate_invitation_token
from acl.operations import permission_required
from base import helpers
from base.viewsets import MultipleDBModelViewSet
from invites.models import Invite
from invites.serializers import InviteGroupMembershipSerializer, InviteSerializer
from outputs.models import Log
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from acl.operations import user_has_permission


class InviteViewSet(MultipleDBModelViewSet):
    serializer_class = InviteSerializer
    queryset = Invite.objects.none()

    def get_queryset(self):
        ids = json.loads(self.request.query_params.get("id", "[]"))

        has_perm = user_has_permission(self.request, self.request.user, self.action, resource_model=Invite,)
        if has_perm:
            queryset = Invite.objects.select_related("workspace_role").prefetch_related(
                "invite_group_memberships__group_role", "invite_group_memberships__group", "groups"
            ).all()
            if ids:
                queryset = queryset.filter(invite_group_memberships__group__in=ids).distinct()

            return queryset
        else:
            return Invite.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, exclude=None)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, exclude=None)
        return Response(serializer.data)

    @permission_required
    def create(self, request, *args, **kwargs):
        request_data = copy.deepcopy(request.data)
        token, exp = generate_invitation_token(
            request_data["email"],
            request.workspace_slug,
            request_data["workspace_role_id"],
            helpers._get_request_lang(request),
        )
        serializer = self.get_serializer(
            data={
                "email": request_data["email"],
                "invite_token": token,
                "invite_estimate_timestamp_invalid": exp,
                "workspace_role_id": request_data["workspace_role_id"],
            }
        )

        if serializer.is_valid(raise_exception=True):
            invitation = serializer.save()

        # Has to be in serializer but my limited skill fail on it :/ @dbyzero
        for id in request_data.get("ids"):
            group_serializer = InviteGroupMembershipSerializer(
                data={
                    "id": id,
                    "group_role_id": request_data.get("group_role_id"),
                    "invite_id": invitation.id,
                }
            )
            if group_serializer.is_valid(raise_exception=True):
                group = group_serializer.save()  # NOQA: F841

        return Response(InviteSerializer(invitation).data, status=status.HTTP_201_CREATED)

    @permission_required
    def destroy(self, request, *args, pk=None, **kwargs):
        return super().destroy(request, *args, pk=pk, **kwargs)

    @permission_required
    def bulk_destroy(self, request, *args, pk=None, **kwargs):
        invite_ids = request.data.get("invite_ids")
        invites = Invite.objects.filter(pk__in=invite_ids)

        nb_invites_deleted = len(invites)
        self.perform_bulk_destroy(invites)

        return Response(data={"nb_invites_deleted": nb_invites_deleted})


@api_view(["POST"])
def refresh(request):
    request_data = copy.deepcopy(request.data)
    token = request_data.get("token")
    invite_id = request_data.get("invite_id")
    workspace = request.META.get("HTTP_X_WORKSPACE", None)

    # Handle 2 cases - resend invitation from `Users` page, resend invitation from `Login` page
    if invite_id:
        invite = Invite.objects.prefetch_related("workspace_role").get(pk=request_data["invite_id"])
    elif token:
        invite = Invite.objects.prefetch_related("workspace_role").get(invite_token=request_data["token"])

    token, exp = generate_invitation_token(
        invite.email,
        workspace,
        str(invite.workspace_role.workspace_role_id),
        helpers._get_request_lang(request),
    )
    invite.invite_token = token
    invite.invite_estimate_timestamp_invalid = exp
    invite.save(using=request.workspace_slug)

    log = Log(
        username=request.user.email if request.user.is_authenticated else None,
        user_id=str(request.user.id) if request.user.is_authenticated else None,
        action_type="RESEND",
        modified_model_name="Invite",
        modified_object_name=invite.email,
        modified_object_id=invite.id,
        role_name=invite.workspace_role.workspace_role_name,
    )
    log.save(using=request.workspace_slug)

    invite_serializer = InviteSerializer(invite)
    return Response(invite_serializer.data)
