from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from munity.users.models import User
from munity.models import MunityModel

class Record(MunityModel):
    previous_value = models.JSONField()
    next_value = models.JSONField()
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    product_object_id = models.UUIDField()
    product_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    product = GenericForeignKey(
        'product_content_type',
        'product_object_id',
    )

    def get_absolute_url(self):
        return f"/records/{self.id}"

    def __str__(self):
        return self.label
