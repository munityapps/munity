import uuid

# from .groups.models import Group

from django.db import models
from django_extensions.db.models import TimeStampedModel


class MunityModel(TimeStampedModel):
    """
    Default base class for munity models
    use uuid for ids
    add creation and update date
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        "workspaces.Workspace", to_field="slug", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        abstract = True

class MunityGroupableModel(models.Model):
    """
    Default base class for munity models
    use uuid for ids
    add creation and update date
    add logs
    add groups
    """
    generic_groups = models.ManyToManyField('generic_groups.GenericGroup', blank=True)

    class Meta:
        abstract = True