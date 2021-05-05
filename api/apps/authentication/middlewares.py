from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from authentication.api_keys import RedisMasterAPIKeys
from authentication.exceptions import TokenDoesNotMatchException, TokenNotFoundException, UserDoesNotExistException
from rest_framework import authentication
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings


class CustomJWTAuthentication(authentication.BaseAuthentication):
    """
    Enrich the behavior of the JWTAuthentication Middleware by:
    - check if the desired routes is in the whitelist. If yes, it skip the token verification part.
    - check if the JWT token is in the header. If not, return an error message.
    """

    def authenticate(self, request):  # NOQA: C901
        # The following two attributes are used by the acl module to automatically grant all permissions if any of them is True
        setattr(request, "is_internal", False)
        setattr(request, "is_master_api_key", False)

        # Case 1: Internal request (coming from other services in the same docker-compose stack)
        if (
            request.META.get("HTTP_X_INTERNAL_REQUEST") is not None
            or settings.DEBUG_SIMULATE_INTERNAL_REQUEST is not False
        ):
            setattr(request, "is_internal", True)
            setattr(request, "workspace_slug", request.META.get("HTTP_X_WORKSPACE", None))
            return None

        # Case 2: API Key
        if (request.META.get("HTTP_X_MASTER_API_KEY") is not None) and (
            RedisMasterAPIKeys().validate_master_api_key(request.META.get("HTTP_X_MASTER_API_KEY"))
        ):
            setattr(request, "is_master_api_key", True)
            setattr(request, "workspace_slug", request.META.get("HTTP_X_WORKSPACE", None))
            return None

        # Case 3: debug.py DEBUG_BYPASS_AUTHENTICATION
        if settings.DEBUG_BYPASS_AUTHENTICATION:
            workspace = request.META.get("HTTP_X_WORKSPACE", None)
            setattr(request, "workspace_slug", workspace)
            try:
                user = User.objects.using(workspace).get(username=settings.DEBUG_BYPASS_AUTHENTICATION_USERNAME)
            except User.DoesNotExist:
                raise APIException(
                    "Possible reasons:\n"
                    f"1) User with username='{settings.DEBUG_BYPASS_AUTHENTICATION_USERNAME}' does not exist in workspace '{workspace}'\n"
                    "2) You are trying to send requests to the api via the frontend or Postman and forgot to comment the debug.py file\n"
                )
            return user, None

        # Case 4: settings.AUTHENTICATION_WHITELIST_ROUTES
        elif request._request.path_info in settings.AUTHENTICATION_WHITELIST_ROUTES:
            setattr(request, "workspace_slug", request.META.get("HTTP_X_WORKSPACE", None))
            return None

        # Case 5: Logged in user with JWT
        else:
            if request.META.get("HTTP_AUTHORIZATION") is None:
                raise TokenNotFoundException(
                    {"detail": _("authorization_token_not_found_in_request_object."), "messages": "Token not found."}
                )

            jwt_authentication = JWTAuthentication()

            header = jwt_authentication.get_header(request)
            if header is None:
                return None

            raw_token = jwt_authentication.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = jwt_authentication.get_validated_token(raw_token)
            workspace = validated_token["workspace"]

            if workspace != request.META.get("HTTP_X_WORKSPACE", None):
                raise TokenDoesNotMatchException("token_error")

            # check if user exists
            user = User.objects.using(workspace).filter(id=validated_token["user_id"])
            if not user:
                raise UserDoesNotExistException("user_not_found")

            # enrich request object with workspace
            setattr(request, "workspace_slug", workspace)

            return self.get_user(validated_token, workspace), None

    def get_user(self, validated_token, workspace_db):
        """
        Attempts to find and return a user using the given validated token.
        """

        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("token_contained_no_recognizable_user_identification"))

        try:
            user = User.objects.using(workspace_db).get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise PermissionDenied("user_not_found")
            # raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_("user_is_inactive"), code="user_inactive")

        return user
