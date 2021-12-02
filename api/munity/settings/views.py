from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from django.db.models import Q

from ..views import MunityViewSet

from .models import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "key",
            "value",
            "workspace",
            "created",
            "modified",
        ]
        model = Settings


class SettingsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "workspace": ["exact", "in"],
            "key": ["exact", "in"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = Settings


class SettingsViewSet(MunityViewSet):
    serializer_class = SettingsSerializer
    filterset_class = SettingsFilter