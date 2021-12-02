from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from views import MunityViewSet

from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "previous_value",
            "next_value",
            "created",
            "user",
            "product",
        ]
        model = Record

class RecordsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "created": ["gt", "gte", "lt", "lte"],
            "user": ["exact"],
            "product": ["exact"],
        }
        model = Record


class RecordsViewSet(MunityViewSet):
    serializer_class = RecordSerializer
    filterset_class = RecordsFilter

