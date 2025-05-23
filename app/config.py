import os

GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "your-username")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "your-repo-name")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
