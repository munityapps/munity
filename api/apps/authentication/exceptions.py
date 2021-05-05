from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class TokenNotFoundException(AuthenticationFailed):
    """
    This Exception is used to return an error in case of the JWT Token is not found in
    the request while the user is accessing restricted part of the API.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authorization token not found in request object.")
    default_code = "token_not_found"


class TokenDoesNotMatchException(AuthenticationFailed):
    """
    This Exception is used to return an error in case of the JWT Token is not found in
    the request while the user is accessing restricted part of the API.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Authorization token workspace not match with url workspace.")
    default_code = "token_workspace_not_match"


class UserDoesNotExistException(AuthenticationFailed):
    """
    This Exception is used to return an error in case of the JWT Token as an invalid user_id
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("User from jwt token does not exists")
    default_code = "user_token_does_not_exist"
