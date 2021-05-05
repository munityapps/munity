from base.serializers import ModelSerializerWithFields
from devices.models import Device
from groups.models import Group
from graphs.models import Graph, PreviewSettings
from rest_framework import serializers


class GraphSerializer(ModelSerializerWithFields):
    class Meta:
        model = Graph
        exclude = ("devices", "groups")

    dashboard_ids = serializers.PrimaryKeyRelatedField(source="dashboards", many=True, read_only=True)
    devices_in = serializers.PrimaryKeyRelatedField(source="devices", queryset=Device.objects.all(), many=True)
    groups_in = serializers.PrimaryKeyRelatedField(source="groups", queryset=Group.objects.all(), many=True)
    _graph_data = serializers.JSONField(source="get_graph_data", read_only=True)
    ids = serializers.SerializerMethodField(read_only=True)

    def get_ids(self, graph):
        ids = [device.pk for device in graph.get_associated_devices()]
        return ids


# A ListSerializer overriding update methods is needed to perform bulk_update query:
# https://github.com/miki725/django-rest-framework-bulk#drf3
# https://www.django-rest-framework.org/api-guide/serializers/#customizing-listserializer-behavior
class PreviewSettingsListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        ret = []
        for data in validated_data:
            preview_settings = instance.get(device=data["device"])
            ret.append(self.child.update(preview_settings, data))
        return ret


class PreviewSettingsSerializer(ModelSerializerWithFields):
    class Meta:
        list_serializer_class = PreviewSettingsListSerializer
        model = PreviewSettings
        exclude = ("device",)

    id = serializers.PrimaryKeyRelatedField(source="device", queryset=Device.objects.all())
