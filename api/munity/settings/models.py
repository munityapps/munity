from django_extensions.db.models import TimeStampedModel
from django.db import models

from ..models import MunityModel

class Settings(MunityModel):
    key = models.CharField(max_length=100)
    value = models.JSONField()

    def __str__(self):
        return f"{self.key}@{self.workspace or 'overmind'}"

    class Meta:
        unique_together = [("key", "workspace")]
