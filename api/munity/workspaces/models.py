from django_extensions.db.models import TimeStampedModel
from django.db import models


class Workspace(TimeStampedModel):
    class Meta:
        ordering = ("slug",)

    disabled = models.BooleanField(default=False)
    slug = models.SlugField(primary_key=True, max_length=50, unique=True)
    name = models.CharField(max_length=258, blank=True, null=False, default="")
    db_connection = models.CharField(max_length=100, blank=True, null=True, default=True)
    icon = models.ForeignKey("files.File", related_name="workspace_icon", on_delete=models.CASCADE, blank=True, null=True, default=None)

    def get_absolute_url(self):
        return f"/workspaces/{self.slug}"

    def __str__(self):
        return self.slug
