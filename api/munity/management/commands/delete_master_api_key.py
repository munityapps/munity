from django.core.management.base import BaseCommand

from authentication.api_keys import RedisMasterAPIKeys


class Command(BaseCommand):
    help = """Remove API Keys master_api_keys allowing permission with X-MASTER-API-KEY
    ex : python manage.py remove_api_master_api_key 2 4
    """

    def add_arguments(self, parser):
        parser.add_argument("ids", nargs="+", type=str)

    def handle(self, *args, **options):
        ids = options.get("ids")
        RedisMasterAPIKeys().delete_master_api_keys(ids)
        self.stdout.write(self.style.SUCCESS(f"Successfully deleting master_api_keys {ids}."))
