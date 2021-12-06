from django.core.management.base import BaseCommand, CommandError
from django.db.models.query_utils import Q
from munity.authorization.models import Role, Permission

class Command(BaseCommand):
    help = 'Initiate Munity with basic authorization'

    def handle(self, *args, **options):
        self.stdout.write("Adding Owner, Admin and User role")
        # (owner_role, _) = Role.objects.update_or_create(
        #     name="Owner"
        # )

        (admin_role, _) = Role.objects.update_or_create(
            name="Admin"
        )

        (user_role, _) = Role.objects.update_or_create(
            name="User"
        )

        # godmode=1
        # owner_role.permissions.set(Permission.objects.all())
        # can do everything but edit/create workspace
        admin_role.permissions.set(Permission.objects.exclude(
            Q(action=["delete", "update", "create"]) &
            Q(ressource__model__in=["workspace"])
        ))
        # readonly
        user_role.permissions.set(Permission.objects.filter(action__in=["list", "retrieve"]))
