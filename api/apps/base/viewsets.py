import json

from users.models import User
from users.serializers import UserSerializer
from acl.operations import permission_required
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework_bulk import BulkModelViewSet


class MultipleDBModelViewSet(BulkModelViewSet):
    """This is a custom DRF ViewSet that is made to connect to the right workspace database
    before performing CRUD operations. Otherwise, operations would be performed on the 'default' database.
    Note: If you want to redefine any of the functions below, you will need to add the @workspace_specific decorator.
    """

    def get_queryset(self):
        try:
            multiple_ids = json.loads(self.request.query_params.get("ids"))
        except (TypeError, json.decoder.JSONDecodeError):
            multiple_ids = None
        if not multiple_ids:
            return self.get_serializer_class().Meta.model.objects.all()
        else:
            return self.get_serializer_class().Meta.model.objects.filter(pk__in=multiple_ids)

    @permission_required
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required
    def retrieve(self, request, *args, pk=None, **kwargs):
        return super().retrieve(request, *args, pk=pk, **kwargs)

    @permission_required
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required
    def update(self, request, *args, pk=None, **kwargs):
        return super().update(request, *args, pk=pk, **kwargs)

    @permission_required
    def partial_update(self, request, *args, pk=None, **kwargs):
        return super().partial_update(request, *args, pk=pk, **kwargs)

    @permission_required
    def destroy(self, request, *args, pk=None, **kwargs):
        return super().destroy(request, *args, pk=pk, **kwargs)

    @permission_required
    def bulk_update(self, request, *args, **kwargs):
        return super().bulk_update(request, *args, **kwargs)

    @permission_required
    def partial_bulk_update(self, request, *args, **kwargs):
        return super().partial_bulk_update(request, *args, **kwargs)

    @permission_required
    def bulk_destroy(self, request, *args, **kwargs):
        ids = json.loads(request.query_params.get("ids"))
        if not ids:
            return super().destroy(request, *args, pk=kwargs.pop("pk"), **kwargs)
        else:
            return super().bulk_destroy(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        ids = self.request.query_params.get("ids", None)
        if ids:
            return super().filter_queryset(queryset.filter(pk__in=json.loads(ids)))
        # returns normal query set if no param
        return super().filter_queryset(queryset)


class NoListMixin:
    """Mixin that defines List operations as not allowed (for use in conjunction with MultipleDBModelViewSet)."""

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)


class NoCreateMixin:
    """Mixin that defines Create operations as not allowed (for use in conjunction with MultipleDBModelViewSet)."""

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)


class NoUpdateMixin:
    """Mixin that defines Update operations as not allowed (for use in conjunction with MultipleDBModelViewSet)."""

    def update(self, request, *args, pk=None, **kwargs):
        raise MethodNotAllowed(self.action)

    def partial_update(self, request, *args, pk=None, **kwargs):
        raise MethodNotAllowed(self.action)

    def bulk_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)

    def partial_bulk_update(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)


class NoDestroyMixin:
    """Mixin that defines Destroy operations as not allowed (for use in conjunction with MultipleDBModelViewSet)."""

    def destroy(self, request, *args, pk=None, **kwargs):
        raise MethodNotAllowed(self.action)

    def bulk_destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed(self.action)


class TestViewSet(MultipleDBModelViewSet):
    """This is just a test viewset. This can be useful if you're tinkering with request attributes."""

    serializer_class = UserSerializer
    queryset = User.objects.none()  # Sentinel queryset: http://www.django-rest-framework.org/api-guide/

    def retrieve(self, request, pk=None):
        """
        Returns whatever you want it to return:
        """
        if pk == "self_dict":
            # self.__dict__:
            return Response({str(k): str(v) for k, v in self.__dict__.items()})
        elif pk == "request_dict":
            # request.__dict__:
            return Response({str(k): str(v) for k, v in request.__dict__.items()})
        elif pk == "request_META":
            # request.META (headers):
            return Response({str(k): str(v) for k, v in request.META.items()})
        elif pk == "dir_request":
            # dir(request):
            return Response({"dir(request)": [str(v) for v in dir(request)]})
        else:
            return Response()

    def list(self, request):
        return Response()
