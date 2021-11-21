from django.contrib.contenttypes.models import ContentType
from django.db import models

from ..models import MunityModel


class Permission(MunityModel):
    ressource = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="munity_permissions"
    )
    action = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ressource}:{self.action}"

    class Meta:
        unique_together = [("ressource", "action")]


class Role(MunityModel):
    name = models.CharField(unique=True, max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        if self.workspace:
            # workspace from MunityModel
            return f"self.name[{self.workspace}]"
        return self.name


DEFAULT_ACTIONS = ["list", "retrieve", "update", "create", "delete"]

def sync_permissions(sender, **kwargs):
    for ct in ContentType.objects.exclude(
        app_label__in=["admin", "silk", "sessions", "contenttypes", "auth"]
    ):
        for action in DEFAULT_ACTIONS:
            _obj, _created = Permission.objects.get_or_create(
                action=action, ressource=ct
            )
