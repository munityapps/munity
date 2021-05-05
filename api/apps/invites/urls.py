from rest_framework_bulk.routes import BulkRouter
from invites import views
from django.conf.urls import include, url

PREFIX = r'^invites/'
router = BulkRouter()

router.register(r"", views.InviteViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
    url(PREFIX + r"refresh$", views.refresh),
]