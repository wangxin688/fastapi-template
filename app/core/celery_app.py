from celery import Celery

from app.core.config import settings


class Config:
    broker = settings.BROKER_URL
    backend = settings.RESULT_BACKEND
    task_acks_late = True
    task_reject_on_worker_lost = True
    worker_max_tasks_per_child = 2
    task_track_started = True
    imports = ("app.api.auth.tasks", "app.api.dcim.tasks")


celery_app = Celery(__name__)

celery_app.config_from_object(Config)
