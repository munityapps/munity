from django_filters import rest_framework as filters
from munity.views import MunityViewSet
from rest_framework import serializers

from .models import GenericGroup

class GenericGroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "label",
            "generic_groups",
            "workspace",
            "created",
            "modified",
        ]
        model = GenericGroup


class GenericGroupsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "label": ["exact", "in", "contains"],
            "generic_groups": ["in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = GenericGroup


class GenericGroupsViewSet(MunityViewSet):
    serializer_class = GenericGroupSerializer
    filterset_class = GenericGroupsFilter
