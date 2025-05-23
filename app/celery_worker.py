from celery import Celery
from app.config import BROKER_URL, BACKEND_URL

celery_app = Celery(
    "worker",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=["app.tasks.github_checker"]
)

celery_app.conf.beat_schedule = {
    "check-github-commits-every-minute": {
        "task": "app.tasks.github_checker.check_for_new_commit",
        "schedule": 60.0,
    },
}

celery_app.conf.timezone = "UTC"
