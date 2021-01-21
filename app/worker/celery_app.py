import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv('.env')


app = Celery(
    'app',
    broker=f"redis://redis:{os.environ.get('REDIS_PORT')}/1",
    include=['app.worker.celery_worker']
)
