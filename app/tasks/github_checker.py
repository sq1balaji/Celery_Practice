import os
import requests
from celery import shared_task
from app.config import GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN

LAST_COMMIT_FILE = "/tmp/last_commit.txt"

@shared_task
def check_for_new_commit():
    commits_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    response = requests.get(commits_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch commits: {response.status_code}")
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

        commit_detail_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits/{latest_sha}"
        commit_detail = requests.get(commit_detail_url, headers=headers).json()

        print("📁 Changed files:")
        for file in commit_detail.get("files", []):
            print(f" - {file['filename']}")

        with open(LAST_COMMIT_FILE, "w") as f:
            f.write(latest_sha)
    else:
        print("✅ No new commit.")
