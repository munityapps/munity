from rest_framework_bulk.routes import BulkRouter
from devices import views
from django.conf.urls import include, url

PREFIX = r'^devices/'
router = BulkRouter()

router.register(r"", views.DeviceViewSet)
router.register(r"page/(?P<page>[^/]+)", views.DeviceViewSet)
router.register(r"page/(?P<page>[^/]+)/step/(?P<step>[^/]+)", views.DeviceViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
    url(PREFIX + r"summary/(?P<id>[^/]+)/page/(?P<page>[^/]+)$", views.device_summary),
    url(PREFIX + r"hardwares$", views.get_all_hardware_ids),
]