from workspace import views
from django.conf import settings
from django.conf.urls import include, url
from base.routers import SingleObjectRouter

PREFIX = r"^workspace/"

# settings route
single_object_router = SingleObjectRouter()
single_object_router.register(r"", views.WorkspaceSettingsViewSet)

urlpatterns = [
    url(PREFIX + r"check-exists$", views.check_exists),
    url(PREFIX + r"check_security_code$", views.check_security_code),
    url(PREFIX + r"recover$", views.recover_my_workspaces),
    url(PREFIX + r"settings/", include(single_object_router.urls)),
    url(PREFIX + r"", views.WorkspaceAPIView.as_view()),
]
