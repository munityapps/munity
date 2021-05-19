from base.serializers import ModelSerializerWithFields
from .models import Settings


class SettingsSerializer(ModelSerializerWithFields):
    class Meta:
        model = Settings
        fields = ["key", "value"]
