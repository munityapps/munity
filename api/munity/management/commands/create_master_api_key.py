from django.core.management.base import BaseCommand

from authentication.api_keys import RedisMasterAPIKeys


class Command(BaseCommand):
    help = "Create an API Key Token allowing permission with X-MASTER-API-KEY"

    def handle(self, *args, **options):
        id, token = RedisMasterAPIKeys().add_master_api_key()
        self.stdout.write(self.style.SUCCESS(f"Successfully generating token {id} : {token}"))
