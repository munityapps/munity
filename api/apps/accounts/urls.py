from rest_framework_bulk.routes import BulkRouter
from accounts import views
from django.conf.urls import include, url

PREFIX = r"^users/"
router = BulkRouter()

router.register(r"", views.UserViewSet)
router.register(r"page/(?P<page>[^/]+)", views.UserViewSet)
router.register(r"page/(?P<page>[^/]+/step/(?P<step>[^/]+))", views.UserViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
    url(PREFIX + r"reset-password$", views.request_reset_password),
    url(PREFIX + r"reset-user-password$", views.reset_user_password, name="reset_user_password"),
    url(PREFIX + r"send-account-activation$", views.send_account_activation),
    url(PREFIX + r"check-account-activation$", views.check_account_activation),
    url(PREFIX + r"invite$", views.invite),
    url(PREFIX + r"register$", views.register),
    url(PREFIX + r"upload/avatar$", views.upload_profile_picture),
    url(PREFIX + r"accounts", include("rest_registration.api.urls")),
    url(PREFIX + r"summary/(?P<user_id>[^/]+)/page/(?P<page>[^/]+)$", views.user_summary),
]
