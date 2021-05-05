from base.serializers import ModelSerializerWithFields
from workspace.models import WorkspaceSettings


class WorkspaceSettingsSerializer(ModelSerializerWithFields):
    class Meta:
        model = WorkspaceSettings
        fields = ["key", "value"]
