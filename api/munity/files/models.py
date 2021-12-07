import uuid
from django_extensions.db.models import TimeStampedModel
from django.db import models

from ..models import MunityModel

def generate_filename(self, filename):
    url = "%s/%s" % (self.workspace if self.workspace else 'overmind', f"{uuid.uuid4()}.{filename.split('.')[-1]}")
    return url

class File(MunityModel):
    name = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=32, blank=True)
    size = models.BigIntegerField(blank=True)
    file = models.FileField(upload_to=generate_filename)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.name}"
