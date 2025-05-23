from celery import Celery
import os
import app.tasks.github_checker

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

celery_app = Celery("app", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Automatically discover tasks in 'app' directory
celery_app.autodiscover_tasks(['app'])
