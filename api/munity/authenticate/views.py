from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.contenttypes.models import ContentType

from ..records.models import Record
from ..users.models import User
from ..users.views import UserSerializer

import jwt


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user.password = "********"
        token["user_at_first_login"] = UserSerializer(user).data

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        response = super().post(request, args, kwargs)
        # we assume that credentials are correct if parent class do not trigg errors

        ctype = ContentType.objects.get_for_model(User)
        accesst_token = response.data.get("access")
        data = jwt.decode(accesst_token, options={"verify_signature": False})

        Record.objects.create(
            action = "login",
            product_object_id = data["user_id"],
            product_content_type = ctype,
            user_id = data["user_id"]
        )

        return response