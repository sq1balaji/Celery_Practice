import os
import requests
from app.celery_worker import celery_app
from app.config import GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN

LAST_COMMIT_FILE = "/tmp/last_commit.txt"

@celery_app.task
def check_for_new_commit():
    url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch commits: {response.status_code}")
        return

    latest_commit = response.json()[0]
    latest_sha = latest_commit["sha"]

    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as f:
            saved_sha = f.read().strip()
    else:
        saved_sha = None

    if latest_sha != saved_sha:
        print(f"🔔 New commit detected: {latest_sha}")
        with open(LAST_COMMIT_FILE, "w") as f:
            f.write(latest_sha)
    else:
        print("✅ No new commit.")
