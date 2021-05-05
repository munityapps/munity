from django.core import management
from django.core.management.base import BaseCommand
from workspace.operations import list_existing_workspaces


class Command(BaseCommand):
    help = "Migrate all Workspace(s) database"

    def add_arguments(self, parser):
        parser.add_argument('--fake', action="store_true", help="Run each migration and fake it, if it already existe")

    def handle(self, *args, **options):
        existing_workspaces = list_existing_workspaces()
        existing_workspaces.insert(0, "default")

        for name in existing_workspaces:
            workspace_slug = name.replace("workspace_", "").replace("_", "-")
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n* Migrating {workspace_slug if workspace_slug != 'default' else 'reference'} Workspace *"
                )
            )

            cmd_args = ["--database", workspace_slug]

            if options.get('fake'):
                cmd_args.insert(0, '--fake-initial')

            management.call_command("migrate", *cmd_args)

        self.stdout.write(self.style.SUCCESS(f"Successfully migrated all Workspaces."))
