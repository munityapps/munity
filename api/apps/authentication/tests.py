from django.conf import settings
from django.conf.urls import url
from django.test import Client, TestCase
from django.test.utils import override_settings

from accounts.models import User
from munity.urls import urlpatterns as base_patterns
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Override urlconf for testing
PREFIX = settings.REST_FRAMEWORK_ROUTER_PREFIX
if PREFIX:
    PREFIX = r"^" + str(PREFIX) + r"/"


@api_view(["GET", "POST"])
def no_authentication_test(request):
    return Response("Hello World! No Authentication!")


@api_view(["GET", "POST"])
def authentication_test(request):
    return Response("Hello World! Authentication.")


urlpatterns = base_patterns + [
    url(PREFIX + r"api/v1/requests-auth", authentication_test),
    url(PREFIX + r"api/v1/requests-noauth", no_authentication_test),
]


@override_settings(ROOT_URLCONF=__name__)
class TestCustomJWTAuthentication(TestCase):
    def setUp(self):

        # Save a fake user in the test database.
        u = User.objects.create_user(username="bonjour", password="tadaaa")
        u.save()

        # Override JWT Whitelist for testing.
        settings.AUTHENTICATION_WHITELIST_ROUTES = ["/api/v1/requests-noauth"]

        self.c = Client()

        response = self.c.post("/api/v1/token/", {"username": "bonjour", "password": "tadaaa"})
        self.refresh_token = response.data["refresh"]
        self.access_token = response.data["access"]

    def test_jwt_authentication(self):

        response = self.c.get("/api/v1/requests-auth", HTTP_AUTHORIZATION=self.access_token)

        # Should return status code 200: Need a token and the token provided is good.
        self.assertEquals(response.status_code, 200)

    def test_whitelist_authentication(self):

        response = self.c.get("/api/v1/requests-noauth")

        # Should return status code 200: no token provided, but route on the whitelist, so no token needed.
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_authentication(self):

        response = self.c.get("/api/v1/requests-auth", HTTP_AUTHORIZATION="Bearer fake-token")

        # Should return status code 403: Need valid token while fake token provided.
        self.assertEqual(response.status_code, 403)
        #  Should return code token not valid.
        self.assertEqual(response.data["code"], "token_not_valid")

    def test_unprovided_token_authentication(self):

        response = self.c.get("/api/v1/requests-auth")

        # Should return status code 403: Need a token while no token provided.
        self.assertEqual(response.status_code, 403)
        #  Should return code token not founded.
        self.assertEqual(response.data["code"], "token_not_found")
