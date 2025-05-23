import os
from urllib.parse import urlparse

# Load environment variables
REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/sq1balaji/Celery_Practice.git")
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# Parse the GitHub repo URL
def parse_github_url(repo_url):
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    raise ValueError("Invalid GitHub repo URL")

GITHUB_REPO_OWNER, GITHUB_REPO_NAME = parse_github_url(REPO_URL)
