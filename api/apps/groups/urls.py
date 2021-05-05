from rest_framework_bulk.routes import BulkRouter
from groups import views
from django.conf.urls import include, url

PREFIX = r"^groups/"
router = BulkRouter()

router.register(r"memberships/users", views.UserGroupMembershipViewSet)
router.register(r"memberships/users/(?P<user_id>[^/]+)", views.UserGroupMembershipViewSet)
router.register(r"memberships/invite", views.InviteGroupMembershipViewSet)
router.register(r"memberships/invites/(?P<invite_id>[^/]+)", views.InviteGroupMembershipViewSet)

router.register(r"", views.GroupViewSet)
router.register(r"page/(?P<page>[^/]+)", views.GroupViewSet)
router.register(r"page/(?P<page>[^/]+/step/(?P<step>[^/]+))", views.GroupViewSet)

urlpatterns = [
    url(PREFIX, include(router.urls)),
    url(PREFIX + r"summary/(?P<id>[^/]+)/page/(?P<page>[^/]+)$", views.group_summary),
]
