# LIBS
import datetime
import json
import time
import uuid
import ast
import jwt
import cloudinary
import cloudinary.api
import cloudinary.uploader

# DJANGO
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from django.db.models import Q

# MUNITY APPS
from base import helpers
from base.viewsets import MultipleDBModelViewSet
from accounts.models import User, UserGroupMembership
from accounts.operations import generate_invitation_token, update_user_password, validate_invitation_token
from accounts.serializers import UserSerializer
from acl.models import GroupRole, WorkspaceRole
from acl.operations import permission_required
from acl.serializers import WorkspaceRoleSerializer
from groups.models import Group
from outputs.emails import ConfirmAccountEmail, ConfirmResetPasswordEmail, ResetPasswordEmail
from munity.settings_acl import DefaultWorkspaceRoleChoice
from outputs.models import Log
from workspace.models import WorkspaceSettings
from invites.models import Invite


class UserViewSet(MultipleDBModelViewSet):
    serializer_class = UserSerializer
    # Sentinel queryset: http://www.django-rest-framework.org/api-guide/permissions/#using-with-views-that-do-not-include-a-queryset-attribute
    queryset = User.objects.none()

    def get_queryset(self):
        ids = json.loads(self.request.query_params.get("id", "[]"))

        queryset = User.objects.all()
        if ids:
            queryset = queryset.filter(group_memberships__group__in=ids).distinct()

        return queryset.select_related("workspace_role").prefetch_related("group_memberships__group_role", "group_memberships__group")

    @permission_required
    def list(self, request, page=None, step=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        is_hide_owner = WorkspaceSettings.objects.filter(key="hide_owner").count()
        if is_hide_owner > 0:
            # Hide owner if Workspace Settings hide owner is true
            hide_owner = ast.literal_eval(WorkspaceSettings.objects.get(key="hide_owner").value)
            if hide_owner:
                queryset = queryset.exclude(workspace_role__workspace_role_name=DefaultWorkspaceRoleChoice.OWNER.value)

        # Pagination
        if page != None:
            serializer = self.get_serializer(queryset, many=True)
            if step == None:
                step = settings.PAGE_SIZE
            count = len(serializer.data)
            if page is not None:

                paginator = Paginator(serializer.data, step)
                try:
                    return Response(data={"count": count, "results": list(paginator.get_page(page))})
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    return Response(data=[])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, exclude=None)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, exclude=None)
        return Response(serializer.data)

    @permission_required
    def update(self, request, *args, pk=None, **kwargs):
        # A user cannot give another user a higher role than his own
        if request.data.get("workspace_role_id"):
            workspace_role_names = [role_choice.value for role_choice in DefaultWorkspaceRoleChoice]
            workspace_role = WorkspaceRole.objects.get(workspace_role_id=request.data["workspace_role_id"])
            if workspace_role_names.index(workspace_role.workspace_role_name) < workspace_role_names.index(
                request.user.workspace_role.workspace_role_name
            ):
                return Response(status=status.HTTP_403_FORBIDDEN)
        if request.data.get("new_password"):
            update_user_password(
                pk=pk, new_password=request.data.get("new_password"), old_password=request.data["old_password"]
            )
        return super().update(request, *args, pk=pk, **kwargs)

    def can_destroy(self, request, pk=None):
        # Users with WorkspaceRole "Owner" cannot be destroyed
        user_to_destroy = User.objects.get(pk=pk)
        user_to_destroy_is_not_an_owner = (
            user_to_destroy.workspace_role.workspace_role_name != DefaultWorkspaceRoleChoice.OWNER.value
            or user_to_destroy.workspace_role.workspace_role_name is None
        )
        return user_to_destroy_is_not_an_owner

    @permission_required
    def destroy(self, request, *args, pk=None, **kwargs):
        if self.can_destroy(request, pk=pk):
            return super().destroy(request, *args, pk=pk, **kwargs)
        else:
            raise PermissionDenied("workspace_owners_cannot_be_deleted")

    @permission_required
    def bulk_destroy(self, request, *args, **kwargs):

        try:
            ids = json.loads(request.query_params.get("ids"))
        except:
            ids = None
        user_ids = request.data.get("user_ids")
        if user_ids:
            users = User.objects.filter(pk__in=user_ids)

            if all(self.can_destroy(request, pk=user_to_destroy.pk) for user_to_destroy in users):
                nb_users_deleted = len(users)
                self.perform_bulk_destroy(users)
                return Response(data={"nb_users_deleted": nb_users_deleted})

        elif not ids:
            return super().destroy(request, *args, pk=kwargs.pop("pk"), **kwargs)
        else:
            filtered_queryset = self.get_queryset()
            if all(self.can_destroy(request, pk=user_to_destroy.pk) for user_to_destroy in filtered_queryset):
                self.perform_bulk_destroy(filtered_queryset)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def send_account_activation(request):
    """
    Creates a token and send by mail for comfirm account.

    Usage example:
    requests.post(
        url='http://{{workspace}}.api.{{host}}/confirm_account/',
        headers={'content-type': 'application/json', 'authorization': 'Bearer {{token}}'},
        data=json.dumps({
            'lang': 'en',
        })
    )
    """
    user = request.data["user"]
    workspace = request.data["workspace"]

    lang = helpers.get_request_lang(request)
    exp = time.mktime(
        (
            datetime.datetime.today() + datetime.timedelta(minutes=settings.ACCOUNT_VALIDATION_KEY_EXPIRATION_MINUTES)
        ).timetuple()
    )

    data = {"workspace": workspace, "email": user["email"], "exp": exp, "lang": lang}

    email_params = {
        "user": user["firstName"],
        "domain": "https://" + workspace + ".app." + settings.DOMAIN_NAME,
        "token": jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode("utf-8"),
    }

    email_factory = ConfirmAccountEmail(email_params)
    email = email_factory.create_email_msg(
        [user.get("email")], lang=helpers.get_request_lang(request), from_email=settings.SUPPORT_MAIL
    )
    email.send()

    if settings.DEBUG:
        return Response(user.get("email"))
    else:
        return Response()


@api_view(["POST"])
def check_account_activation(request):
    """
    Validate the confirmation account token and return success.

    Usage example:
    requests.get(
        url='http://{{workspace}}.api.{{host}}/activate_confirm_account/?uidb64={{confirm_uid}}&workspaceb64={{confirm_workspace}}&token={{confirm_token}}',
        headers={'content-type': 'application/json'},
    )
    """
    token = request.data["token"]

    try:
        body = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], option={"require_exp": True})
    except jwt.exceptions.ExpiredSignatureError:
        raise ValidationError("expired_token")
    except jwt.exceptions.InvalidTokenError:
        raise ValidationError("token_error")
    try:
        user = User.objects.using(body["workspace"]).get(username=body.get("email", None))
        user.is_active = True
        user.save(using=body["workspace"], update_fields=["is_active"])
        return Response()
    except (User.DoesNotExist):
        raise NotFound("user_not_found")


@api_view(["POST"])
def request_reset_password(request):
    """
    Handle requests for password reset.
    Create a password reset token and send it by email.

    Usage example:
    requests.post(
        url='http://{{workspace}}.api.{{host}}/create_workspace/',
        headers={'content-type': 'application/json'},
        data=json.dumps({
            'lang': 'en',
            'email: {{email}}'
        })
    )
    """

    workspace = request.META.get("HTTP_X_WORKSPACE", None)
    lang = helpers.get_request_lang(request)
    try:
        user = User.objects.using(workspace).get(username__iexact=request.data["email"])
    except (User.DoesNotExist):
        raise NotFound("user_not_found")

    exp = time.mktime(
        (
            datetime.datetime.today() + datetime.timedelta(minutes=settings.RESET_PASSWORD_KEY_EXPIRATION_MINUTES)
        ).timetuple()
    )

    data = {"workspace": workspace, "uid": str(user.pk), "email": user.email, "exp": exp, "lang": lang}

    email_params = {
        "user": user,
        "domain": "https://" + workspace + ".app." + settings.DOMAIN_NAME,
        "token": jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode("utf-8"),
    }
    email_factory = ResetPasswordEmail(email_params)
    email = email_factory.create_email_msg([user.email], lang=lang, from_email=settings.SUPPORT_MAIL)
    email.send()

    if settings.DEBUG:
        email_params["user"] = str(user)
        return Response(email_params)
    else:
        return Response()


@api_view(["POST", "GET"])
def reset_user_password(request):
    """
        Reset user password if wall with post
        Check token validity if call with get

        Usage example:
        request.post(
            url='http://{{workspace}}.api.{{host}}/users/reset-user-password?token={{token}}'
            headers={'content-type': 'application/json'},
            body={
                'new_ password': {{new_password}}
            }
        )

        request.get(
            url='http://{{workspace}}.api.{{host}}/users/reset-user-password?token={{token}}'
        )
    """

    token = request.query_params.get("token")
    workspace = request.META.get("HTTP_X_WORKSPACE")
    new_password = request.data.get("new_password")

    try:
        body = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], option={"require_exp": True})
        if body["workspace"] != workspace:
            raise ValidationError("invalid_workspace")
    except jwt.exceptions.ExpiredSignatureError:
        raise ValidationError("expired_token")
    except jwt.exceptions.InvalidTokenError:
        raise ValidationError("token_error")
    # Just check the token and return email
    if request.method == "GET":
        body.pop("exp")
        body.pop("uid")
        body.pop("lang")
        return Response()

    user = User.objects.using(workspace).get(pk=body["uid"])

    user.set_password(new_password)
    user.save(using=workspace)

    email_params = {"user": user, "support_mail": settings.SUPPORT_MAIL}
    email_factory = ConfirmResetPasswordEmail(email_params)
    email = email_factory.create_email_msg([user.email], lang=body["lang"], from_email=settings.SUPPORT_MAIL)
    email.send()

    return Response()


@api_view(["POST"])
def invite(request):
    """
    Creates a token and send by mail to new user for invite this one.

    Usage example:
    requests.post(
        url='http://{{workspace}}.api.{{host}}/invite/',
        headers={'content-type': 'application/json', 'authorization': 'Bearer {{token}}',
        data=json.dumps({
            'lang': 'en',
            'email': ['toto@orange.com', 'titi@sfr.fr'],
            'group': ['group1', 'group2']
        })
    )
    """
    for email in request.data["email"]:
        if User.objects.using(request.workspace_slug).filter(username=email).exists():
            raise PermissionDenied("email_already_exist")
    for email in request.data["email"]:
        generate_invitation_token(email, request.workspace_slug, None, helpers.get_request_lang(request))
    return Response()


@api_view(["GET"])
def accept_invite(request):
    """
    Validate the token and return new user informations (mail and groups).

    Usage example:
    requests.get(
        url='http://{{workspace}}.api.{{host}}/accept_invite/?token={{token}}',
        headers={'content-type': 'application/json'},
    )
    """
    body, status_code = validate_invitation_token(request.GET["token"], request.META.get("HTTP_X_WORKSPACE", None))
    return Response()


@api_view(["PUT", "POST"])
def upload_profile_picture(request):
    """
    Endpoint called to upload the profile picture of an user
    Once the profile picture is on the server we upload it to cloudinary
    Then we save the picture url to the database and return it to the client
    """

    try:
        workspace = helpers.get_workspace_slug_from_request(request=request)
        user = request.user
    except:
        return Response(status=403)

    picture_url = None
    response = Response({"url_picture": ""})

    if request.data["profile_picture"]:
        file = request.FILES["profile_picture"]
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )
        picture = cloudinary.uploader.upload(file, public_id=workspace + "/" + str(user.id))
        picture_url = picture["secure_url"]
        response = Response({"url_picture": picture_url})

    user = User.objects.get(pk=user.pk)
    user.profile_picture_url = picture_url
    user.save()

    return response



@api_view(["POST", "GET"])
def register(request):
    """
    Register new user for the workspace from URL or Just check invit token.
    That implies creating a new user for the workspace.
    That implies creating a new role user for the workspace if not exist.

    Usage example:
    # For register:
    requests.post(
        url='http://{{workspace}}.api.{{host}}/register?token={{invitation_token}}',
        headers={'content-type': 'application/json'},
        data=json.dumps({
            'firstname': 'john',
            'lastname': 'doe',
            'password': 'azerty',
        })
    )
    # For check token:
    requests.get(
        url='http://{{workspace}}.api.{{host}}/register?token={{invitation_token}}',
    )
    """
    try:
        workspace_slug = request.META.get("HTTP_X_WORKSPACE")
    except:
        raise PermissionDenied("missing_workspace")

    # Check whether the invitation token is valid
    body, status_code = validate_invitation_token(request.GET["token"], workspace_slug)

    if request.method == "GET":
        return Response(body)

    if body.get("mail", "") == "":
        email = request.data["email"]
    else:
        email = body.get("mail")

    # clean up phone number
    tel = request.data.get("tel", "")
    if tel != "" and tel[0] == "0":
        tel = "+33" + tel[1:]

    # Check if username and email already exist
    if User.objects.using(workspace_slug).filter(username=email).exists():
        raise PermissionDenied(detail="username_already_exists")

    # if not exist, create user role
    user_workspace_role, __ = WorkspaceRole.objects.db_manager(workspace_slug).get_or_create(
        workspace_role_name=DefaultWorkspaceRoleChoice.USER.value
    )

    # workspace role handling just in case
    if not body.get("workspace_role_id"):
        print("no assigned workspace role")
    else:
        # check groups exist, removes dead ones
        if WorkspaceRole.objects.filter(pk=uuid.UUID(body["workspace_role_id"])):
            body["workspace_role"] = WorkspaceRoleSerializer(
                WorkspaceRole.objects.get(pk=uuid.UUID(body["workspace_role_id"]))
            ).data
            user_workspace_role = WorkspaceRole.objects.get(pk=uuid.UUID(body["workspace_role_id"]))

    body.pop("workspace_role_id")
    # Using the create_user function, django automatically salts and hashes the password
    # with the pbkdf2_sha256 algorithm.
    user = User.objects.db_manager(workspace_slug).create_user(
        username=email,
        email=email,
        telephone=tel,
        password=request.data["password"],
        workspace_role=user_workspace_role,
        first_name=request.data["firstname"],
        last_name=request.data["lastname"],
        social_id="",
        preferred_language=request.data.get("lang", "en"),
    )

    # Log `Register` activity
    log = Log(
        action_type="REGISTER (FROM INVITATION)",
        modified_model_name="User",
        modified_object_name=email,
        modified_object_id=str(user.id),
        username=email,
        user_id=str(user.id),
    )
    log.save()

    # if user was invited, delete is token from the DB
    if request.GET.get("token") and Invite.objects.filter(invite_token=request.GET["token"]).exists():
        Invite.objects.get(invite_token=request.GET["token"]).delete()

    try:
        for g in body["groups"]:
            group = Group.objects.get(pk=g["id"])
            group_role = GroupRole.objects.get(pk=g["group_role_id"])
            UserGroupMembership(user=user, group=group, group_role=group_role).save(using=workspace_slug)
    except Exception as e:
        return Response(e.__dict__, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=body, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def user_summary(request, user_id, page):
    """
    Gets user's log data

    Usage example:
    requests.get(
        url='http://{{workspace}}.api.{{host}}/user_summary?user_id={{user_id}}',
        headers={'content-type': 'application/json'},
    )

    Possible output:
    [
        {
            "username": "jessica@iot-valley.fr",
            "action_type": "LOGIN",
            "modified_model_name": "",
            "modified_object_name": "",
            "name": null,
            "role_name": null,
            "workspace_name": "users2",
            "created_at": "2019-07-15T14:13:53.301893Z",
            "modification": null,
            "modified_object_id": null,
            "user_id": "61f27af2-9c79-42f1-8be9-1545d83b9aab"
        },
        {
            "username": "jessica@iot-valley.fr",
            "action_type": "LOGIN",
            "modified_model_name": "",
            "modified_object_name": "",
            "name": null,
            "role_name": null,
            "workspace_name": "users2",
            "created_at": "2019-07-15T14:12:15.295981Z",
            "modification": null,
            "modified_object_id": null,
            "user_id": "61f27af2-9c79-42f1-8be9-1545d83b9aab"
        },
        {
            "username": "jessica@iot-valley.fr",
            "action_type": "LOGIN",
            "modified_model_name": "",
            "modified_object_name": "",
            "name": null,
            "role_name": null,
            "workspace_name": "users2",
            "created_at": "2019-07-15T14:11:56.521587Z",
            "modification": null,
            "modified_object_id": null,
            "user_id": "61f27af2-9c79-42f1-8be9-1545d83b9aab"
        },
        {
            "username": "jessica@iot-valley.fr",
            "action_type": "LOGIN",
            "modified_model_name": "",
            "modified_object_name": "",
            "name": null,
            "role_name": null,
            "workspace_name": "users2",
            "created_at": "2019-07-15T14:10:11.725345Z",
            "modification": null,
            "modified_object_id": null,
            "user_id": "61f27af2-9c79-42f1-8be9-1545d83b9aab"
        }
    ]
    """
    # Get workspace slug
    try:
        workspace_slug = request.workspace_slug
    except:
        raise PermissionDenied("missing_workspace")
    if user_id is None:
        raise ValidationError("missing_params")
    # Get log list associated with user
    logs = (
        Log.objects.filter(Q(modified_object_id=user_id) | Q(user_id=user_id))
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
        out_logs = list(paginator.page(page))
    except PageNotAnInteger:
        # If page is not an integer, raise exception
        ValidationError("page_number_invalid")
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return Response(data=[])
    count = logs.count()
    return Response(data={"count": count, "summary": out_logs})
