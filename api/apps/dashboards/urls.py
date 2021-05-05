from rest_framework_bulk.routes import BulkRouter
from dashboards import views
from django.conf.urls import include, url

PREFIX = r"^dashboards/"

router = BulkRouter()

router.register(r"", views.DashboardViewSet)
router.register(r"page/(?P<page>[^/]+)", views.DashboardViewSet)
router.register(r"page/(?P<page>[^/]+/step/(?P<step>[^/]+))", views.DashboardViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
]
