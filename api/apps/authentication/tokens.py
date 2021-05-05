from django.contrib.auth import authenticate
from six import text_type

from accounts.models import User
from authentication.exceptions import UserDoesNotExistException
from outputs.models import Log
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    def get_token_custom(self, user, workspace):
        token = super(CustomObtainPairSerializer, self).get_token(user)
        token["workspace"] = workspace
        return token

    def log_login(self, user, workspace):
        log = Log(
            action_type="LOGIN",
            modified_model_name="",
            modified_object_name="",
            username=user.email,
            user_id=str(user.id),
        )
        log.save(using=workspace)

    def validate(self, attrs):
        try:
            self.user = authenticate(
                **{
                    self.username_field: attrs[self.username_field],
                    "workspace": self.initial_data["workspace"],
                    "password": attrs["password"],
                }
            )
        except AttributeError:
            raise APIException(
                "You are probably trying to send requests to the api via the frontend or Postman and forgot to comment the debug.py file."
            )

        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError("bad_credentials")

        self.log_login(self.user, self.initial_data["workspace"])

        refresh = self.get_token_custom(self.user, self.initial_data["workspace"])

        data = {}
        data["refresh"] = text_type(refresh)
        data["access"] = text_type(refresh.access_token)

        return data


class CustomObtainPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        # check if user exists
        user = User.objects.using(refresh.get("workspace")).filter(id=refresh.get("user_id"))
        if not user:
            raise UserDoesNotExistException("user_not_found")

        data = {"access": text_type(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data["refresh"] = text_type(refresh)

        return data


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    def post(self, request, format=None):
        if request.user.is_authenticated:
            log = Log(
                action_type="LOGOUT",
                modified_model_name="",
                modified_object_name="",
                username=request.user.email,
                user_id=str(request.user.id),
            )
            log.save(using=request.workspace_slug)
        return Response()


token_obtain_pair = CustomObtainPairView.as_view()
token_refresh = CustomTokenRefreshView.as_view()
logout = LogoutView.as_view()
