"""projets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from munity.rest import overmind_router, workspace_router
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Munity Api",
        default_version="v1",
        description="Munity Api description",
        terms_of_service="https://munityapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@munityapp.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


docUrls = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

apiUrls = [
    path("", include(overmind_router.urls)),
    path("", include(workspace_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(docUrls)),
]

urlpatterns = [
    path("v1/", include((apiUrls, "api"), namespace="v1")),
    path("", RedirectView.as_view(url="/v1")),
    path("doc", RedirectView.as_view(url="/v1/redoc")),
    path("admin/", admin.site.urls),
    path("silk/", include("silk.urls", namespace="silk")),
]
# if settings.DEBUG:
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
