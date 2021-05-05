from rest_framework_bulk.routes import BulkRouter
from acl import views
from django.conf.urls import include, url

PREFIX = r"^acl/"
router = BulkRouter()

router.register(r"group", views.GroupACLViewSet)
router.register(r"group-roles", views.GroupRoleViewSet)
router.register(r"group-actions", views.GroupActionViewSet)
router.register(r"group-resources", views.GroupResourceViewSet)

router.register(r"workspace", views.WorkspaceACLViewSet)
router.register(r"workspace-roles", views.WorkspaceRoleViewSet)
router.register(r"workspace-actions", views.WorkspaceActionViewSet)
router.register(r"workspace-resources", views.WorkspaceResourceViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
]
