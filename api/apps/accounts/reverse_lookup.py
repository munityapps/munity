from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

import redis
from accounts.models import User
from singleton_decorator import singleton


@singleton
class RedisUserWorkspaceReverseLookup:
    """This is used to find the workspaces a User is registered in, given their email address.
    Uses Redis Sets as values.
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_LOOKUP["HOST"],
            port=settings.REDIS_LOOKUP["PORT"],
            db=settings.REDIS_LOOKUP["DB_NUMBERS"]["USER_WORKSPACE_MAP"],
        )

    def add_workspace_to_user(self, user_email, workspace_slug):
        return self.redis.sadd(user_email, workspace_slug)

    def remove_workspace_from_user(self, user_email, workspace_slug):
        return self.redis.srem(user_email, workspace_slug)

    def get_workspaces_for_user(self, user_email):
        workspace_slugs = self.redis.smembers(user_email)
        return list(map(bytes.decode, workspace_slugs))


@receiver(post_save, sender=User)
def __sync_user_save_with_redis(instance, created, using, update_fields, signal, sender, **kwargs):
    """Signal handler for when a User has been saved."""
    workspace_slug = using
    if created:
        RedisUserWorkspaceReverseLookup().add_workspace_to_user(instance.email, workspace_slug)


@receiver(pre_delete, sender=User)
def __sync_user_delete_with_redis(instance, using, signal, sender, **kwargs):
    """Signal handler for when a User has been deleted."""
    workspace_slug = using
    RedisUserWorkspaceReverseLookup().remove_workspace_from_user(instance.email, workspace_slug)
