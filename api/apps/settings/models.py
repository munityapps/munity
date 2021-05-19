import uuid
from django.db import models


class Settings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    key = models.CharField(max_length=64, unique=True, null=True)
    value = models.TextField(blank=True, default="")


    def __repr__(self):
        return f"<{self.__class__.__name__}>"
