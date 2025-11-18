from fastapi import FastAPI, Request
from datetime import datetime
import json

app = FastAPI()

LOG_FILE = "payloads.txt"

@app.get("/")
def root():
    return {"message": "Empty API running"}

@app.post("/save")
async def save_payload(request: Request):
    """
    Accept ANY payload (JSON, text, form) and save it.
    """
    try:
        # Try JSON payload
        data = await request.json()
    except:
        # Fallback: raw text
        raw = await request.body()
        data = raw.decode("utf-8")

    # Create log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "payload": data
    }

    # Save to file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Return clean JSON response
    return {
        "message": "Payload saved successfully",
        "logged": entry
    }
