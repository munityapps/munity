from authentication.tokens import CustomObtainPairView, CustomTokenRefreshView, LogoutView
from django.conf.urls import include, url
from rest_framework_simplejwt.views import TokenVerifyView

PREFIX = r"^auth/"

urlpatterns = [
    url(PREFIX + r"oauth/", include("social_django.urls", namespace="social")),
    url(PREFIX + r"token/verify$", TokenVerifyView.as_view(), name="token_verify"),
    url(PREFIX + r"token/refresh$", CustomTokenRefreshView.as_view(), name="token_refresh"),
    url(PREFIX + r"token$", CustomObtainPairView.as_view(), name="token_obtain_pair"),
    url(PREFIX + r"logout$", LogoutView.as_view(), name="logout"),
]
