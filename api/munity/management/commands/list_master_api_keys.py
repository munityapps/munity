from django.core.management.base import BaseCommand

from authentication.api_keys import RedisMasterAPIKeys


class Command(BaseCommand):
    help = "List API Keys Tokens allowing permission with X-MASTER-API-KEY"

    def handle(self, *args, **options):
        master_api_keys = RedisMasterAPIKeys().get_master_api_keys()
        self.stdout.write(self.style.SUCCESS(f"master_api_keys : "))
        for master_api_key_id, master_api_key in master_api_keys.items():
            self.stdout.write(self.style.SUCCESS(f"{master_api_key_id} : {master_api_key}"))
