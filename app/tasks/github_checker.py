import os
import requests
from celery import shared_task
from app.celery_worker import celery_app
from app.config import GITHUB_REPO_OWNER, GITHUB_REPO_NAME, GITHUB_TOKEN

# LAST_COMMIT_FILE = "/tmp/last_commit.txt"

# @celery_app.task
# def check_for_new_commit():
#     url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
#     headers = {"Accept": "application/vnd.github.v3+json"}
#     if GITHUB_TOKEN:
#         headers["Authorization"] = f"token {GITHUB_TOKEN}"

#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Failed to fetch commits: {response.status_code}")
#         return

#     latest_commit = response.json()[0]
#     latest_sha = latest_commit["sha"]

#     if os.path.exists(LAST_COMMIT_FILE):
#         with open(LAST_COMMIT_FILE, "r") as f:
#             saved_sha = f.read().strip()
#     else:
#         saved_sha = None

#     if latest_sha != saved_sha:
#         print(f"🔔 New commit detected: {latest_sha}")
#         with open(LAST_COMMIT_FILE, "w") as f:
#             f.write(latest_sha)
#     else:
#         print("✅ No new commit.")


# import os
# import requests


# Your repo URL (you can make this dynamic later if needed)
REPO_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

@shared_task
def check_for_new_commit():
    # Extract repo owner and name from URL
    parts = REPO_URL.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(commits_url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        latest_commit_sha = commits[0]['sha']

        # File to track last seen commit SHA
        sha_file = "latest_commit.txt"
        if os.path.exists(sha_file):
            with open(sha_file, "r") as f:
                old_sha = f.read().strip()
        else:
            old_sha = ""

        if latest_commit_sha != old_sha:
            print(f"🔔 New commit detected: {latest_commit_sha}")

            # Fetch changed files from commit details
            commit_detail_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{latest_commit_sha}"
            commit_detail = requests.get(commit_detail_url, headers=headers).json()

            print("📁 Changed files:")
            for file in commit_detail.get("files", []):
                print(f" - {file['filename']}")

            with open(sha_file, "w") as f:
                f.write(latest_commit_sha)
        else:
            print("✅ No new commit.")
    else:
        print(f"❌ Failed to fetch commits: {response.status_code}")
