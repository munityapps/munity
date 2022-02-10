import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projects.settings")

celery_app = Celery("munity")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def hello(self, a, b):
    """
    a, b = 2, 1
    r = hello.apply_async(args=(a, b))
    print(r.get())
    """
    return f"hello world: {a+b}"


