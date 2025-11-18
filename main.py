from fastapi import FastAPI, Request
from datetime import datetime
import json
import logging
import sys

app = FastAPI()

# Configure logger at INFO level so Uvicorn will show it
logger = logging.getLogger("uvicorn")  # use uvicorn logger so Render will show it
logger.setLevel(logging.INFO)

LOG_FILE = "payloads.txt"

@app.get("/")
def root():
    return {"message": "Empty API running"}

@app.post("/save")
async def save_payload(request: Request):
    try:
        data = await request.json()
    except Exception:
        raw = await request.body()
        data = raw.decode("utf-8")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "payload": data
    }

    # Save to file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Response we return
    response_json = {
        "status": "saved",
        "data": entry["payload"]
    }

    # 1) Print to stdout (works locally) and flush immediately
    print(json.dumps(response_json, indent=2, ensure_ascii=False), flush=True)

    # 2) Also log with uvicorn logger (ensures it appears in Render logs)
    logger.info(json.dumps(response_json, ensure_ascii=False))

    return response_json
