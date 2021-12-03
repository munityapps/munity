from django_filters import rest_framework as filters
from munity.views import MunityViewSet
from rest_framework import serializers
from pprint import pprint

from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "name",
            "file",
            "type",
            "size",
            "workspace",
            "created",
            "modified",
        ]
        model = File
    def create(self, validated_data):
        file = validated_data.get('file')
        validated_data['size'] = file.size
        validated_data['name'] = file.name
        validated_data['type'] = file.content_type
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return instance.update(**validated_data)


class FileFilter(filters.FilterSet):
    class Meta:
        fields = {
            "id": ["exact", "in"],
            "name": ["exact", "in", "contains"],
            "workspace": ["exact", "in"],
            "type": ["exact", "in", "contains"],
            "size": ["gt", "gte", "lt", "lte"],
            "created": ["gt", "gte", "lt", "lte"],
            "modified": ["gt", "gte", "lt", "lte"],
        }
        model = File


class FileViewSet(MunityViewSet):
    serializer_class = FileSerializer
    filterset_class = FileFilter