from base.serializers import ModelSerializerWithFields
from devices.models import Device
from groups.models import Group
from rest_framework import serializers
from django.conf import settings


class DeviceSerializer(ModelSerializerWithFields):
    class Meta:
        model = Device
        exclude = ("groups", "created_at", "updated_at", "last_triggered_timestamps")

    ids = serializers.PrimaryKeyRelatedField(
        source="groups", queryset=Group.objects.all(), many=True, required=False
    )
    last_values = serializers.JSONField(source="get_graph_data", read_only=True)
