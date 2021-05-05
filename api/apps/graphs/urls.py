from rest_framework_bulk.routes import BulkRouter
from graphs import views
from django.conf.urls import include, url

PREFIX = r'^graphs/'
router = BulkRouter()

router.register(r"", views.GraphViewSet)
router.register(r"preview-settings", views.PreviewSettingsViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
]