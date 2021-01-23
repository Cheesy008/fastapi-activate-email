from celery import Celery

from ..constants import REDIS_PORT

app = Celery(
    'app',
    broker=f"redis://redis:{REDIS_PORT}/1",
    include=['app.worker.celery_worker']
)
