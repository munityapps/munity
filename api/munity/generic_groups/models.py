from django.db import models

from ..models import MunityModel

class GenericGroup(MunityModel):
    label = models.CharField(max_length=255)
    class Meta:
        verbose_name="Generic group"
        verbose_name_plural="Generic groups"

    def get_absolute_url(self):
        return f"/generic_groups/{self.id}"

    def __str__(self):
        return self.label
