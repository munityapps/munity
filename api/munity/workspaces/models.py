from django_extensions.db.models import TimeStampedModel
from django.db import models


class Workspace(TimeStampedModel):
    slug = models.SlugField(primary_key=True, max_length=50, unique=True)
    db_connection = models.CharField(max_length=100, blank=True, null=True)

    def get_absolute_url(self):
        return f"/workspaces/{self.slug}"

    def __str__(self):
        return self.slug
