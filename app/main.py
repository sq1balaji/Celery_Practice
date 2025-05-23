from fastapi import FastAPI
from app.tasks.github_checker import check_for_new_commit

app = FastAPI()

@app.get("/trigger-check")
def trigger_check():
    check_for_new_commit.delay()
    return {"status": "check task triggered"}
