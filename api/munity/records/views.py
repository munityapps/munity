from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from ..views import MunityViewSet

from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "diff_value",
            "previous_value",
            "created",
            "user",
            "product_object_id",
            "product_content_type",
            "action",
        ]
        model = Record

class RecordsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "created": ["gt", "gte", "lt", "lte"],
            "user": ["exact"],
        }
        model = Record


class RecordsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        model = self.serializer_class.Meta.model

        # filter request to current model workspace
        # if "workspace_pk" in self.kwargs:
        #     return model.objects.filter(action="login").filter(action="login").filter(workspace=self.kwargs["workspace_pk"])
        return model.objects.filter(action="login")

    serializer_class = RecordSerializer
    filterset_class = RecordsFilter

