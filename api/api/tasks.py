from munity import celery_app
from celery import shared_task

@celery_app.task
def test(msg):
    print(msg)

@shared_task
def test2(msg):
    print(msg)