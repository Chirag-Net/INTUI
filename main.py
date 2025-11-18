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
        data = await request.json()
    except:
        raw = await request.body()
        data = raw.decode("utf-8")

    # Create log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "payload": data
    }

    # Save to file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    # Create API response
    response_json = {
        "message": "Payload saved successfully",
        "logged": entry
    }

    # ⭐ Print response JSON so it appears in Render Logs
    print(json.dumps(response_json, indent=2))

    return response_json
