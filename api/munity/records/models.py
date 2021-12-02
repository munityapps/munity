import uuid

from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_extensions.db.models import TimeStampedModel

from ..users.models import User
from ..workspaces.models import Workspace

class Record(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    previous_value = models.JSONField(null=True)
    diff_value = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    workspace = models.ForeignKey(Workspace, on_delete=SET_NULL, null=True)
    product_object_id = models.UUIDField()
    product_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    product = GenericForeignKey(
        'product_content_type',
        'product_object_id',
    )
    action = models.CharField(max_length=64, null=False, default="")