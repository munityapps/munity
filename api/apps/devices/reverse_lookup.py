from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

import redis
from devices.models import Device
from singleton_decorator import singleton


@singleton
class RedisDeviceReferenceWorkspaceReverseLookup:
    """This is used to find the workspaces a Device is registered in, given their reference.
    Uses Redis Strings as values.
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_LOOKUP["HOST"],
            port=settings.REDIS_LOOKUP["PORT"],
            db=settings.REDIS_LOOKUP["DB_NUMBERS"]["DEVICE_WORKSPACE_MAP"],
        )

    def _index_reference(self, reference, workspace_slug):
        return self.redis.set(reference, workspace_slug)

    def _unindex_reference(self, reference):
        return self.redis.delete(reference)

    def get_workspace_slug_for_device(self, reference):
        value = self.redis.get(reference)
        return (None if not value else value.decode())


@receiver(post_save, sender=Device)
def __sync_device_save_with_redis(instance, created, using, update_fields, signal, sender, **kwargs):
    """Signal handler for when a Device has been saved."""
    workspace_slug = using
    if created:
        RedisDeviceReferenceWorkspaceReverseLookup()._index_reference(instance.reference, workspace_slug)


@receiver(pre_delete, sender=Device)
def __sync_device_delete_with_redis(instance, using, signal, sender, **kwargs):
    """Signal handler for when a Device has been deleted."""
    RedisDeviceReferenceWorkspaceReverseLookup()._unindex_reference(instance.reference)
