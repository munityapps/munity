from django.conf import settings
from django.utils import timezone

import jwt
import redis
from singleton_decorator import singleton


@singleton
class RedisMasterAPIKeys:
    """
    This is used to create and retrieve tokens for API Token authentification.
    Token is represented as a str 'token_id token' in redis
    Token is represented as a dict {token_id: token} in self.get_tokens()
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_LOOKUP["HOST"],
            port=settings.REDIS_LOOKUP["PORT"],
            db=settings.REDIS_LOOKUP["DB_NUMBERS"]["MASTER_API_KEYS"],
            decode_responses=True,  # Important : otherwise redis response are bytes
        )

    def _create_master_api_key(self):
        payload = {"iat": str(timezone.now()), "sub": "master_api_key"}
        return jwt.encode(payload, settings.API_SECRET_KEY, algorithm="HS256").decode("utf-8")

    def add_master_api_key(self):
        master_api_key = self._create_master_api_key()
        master_api_key_id = max(self.get_master_api_keys().keys() or [-1]) + 1
        self.redis.lpush("master_api_keys", self.to_redis_master_api_key(master_api_key_id, master_api_key))
        return master_api_key_id, master_api_key

    def get_master_api_keys(self):
        master_api_keys = self.redis.lrange("master_api_keys", 0, -1)
        return {int(master_api_key.split()[0]): master_api_key.split()[1] for master_api_key in master_api_keys}

    def delete_master_api_keys(self, master_api_key_ids):
        master_api_keys = self.get_master_api_keys()
        for master_api_key_id in master_api_key_ids:
            master_api_key = master_api_keys.get(int(master_api_key_id))
            if master_api_key:
                self.redis.lrem("master_api_keys", 1, self.to_redis_master_api_key(master_api_key_id, master_api_key))

    def cleanup_master_api_keys(self):
        self.redis.delete("master_api_keys")

    def validate_master_api_key(self, master_api_key):
        return master_api_key in self.get_master_api_keys().values()

    def to_redis_master_api_key(self, master_api_key_id, master_api_key):
        return str(master_api_key_id) + " " + master_api_key
