from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "munity.authorization"

    def ready(self):
        from .models import sync_permissions
        post_migrate.connect(sync_permissions, sender=self)
