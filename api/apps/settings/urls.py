from rest_framework_bulk.routes import BulkRouter
from . import views
from django.conf.urls import include, url

PREFIX = r"^settings/"
router = BulkRouter()

router.register(r"", views.SettingsViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
]
