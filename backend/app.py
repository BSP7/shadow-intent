from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List, Dict
from datetime import datetime
import threading
import time

from models import DeviceLog, IntentResult
from feature_extractor import extract_features
from intent_engine import calculate_intent

app = FastAPI(title="Shadow Intent Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store
device_store: Dict[str, IntentResult] = {}
alert_history: List[Dict] = []

def process_log(log: DeviceLog):
    features = extract_features(log)
    score, status, evidence, recommended_action = calculate_intent(features)
    
    result = IntentResult(
        device_id=log.device_id,
        score=score,
        status=status,
        evidence=evidence,
        recommended_action=recommended_action,
        last_updated=datetime.now()
    )
    
    device_store[log.device_id] = result
    
    if status == "High Risk":
        alert = {
            "device_id": log.device_id,
            "score": score,
            "timestamp": datetime.now(),
            "message": f"Shadow Intent Alert: {status} behavior detected",
            "evidence": evidence,
            "recommended_action": recommended_action
        }
        # Avoid duplicate alerts being spammed
        if not alert_history or (alert_history[-1]["device_id"] != log.device_id or (datetime.now() - alert_history[-1]["timestamp"]).seconds > 10):
             alert_history.append(alert)
             if len(alert_history) > 100:
                 alert_history.pop(0)
    
    return result

@app.get("/")
def read_root():
    return {"status": "Shadow Intent System Online"}

@app.post("/log", response_model=IntentResult)
async def ingest_log(log: DeviceLog):
    return process_log(log)

@app.get("/devices", response_model=List[IntentResult])
async def get_devices():
    devices = list(device_store.values())
    return sorted(devices, key=lambda x: x.score, reverse=True)

@app.get("/alerts")
async def get_alerts():
    return alert_history

@app.on_event("startup")
async def startup_event():
    # Simulation removed: System now depends on real network traffic ingestion
    print("Backend ready. Waiting for live network logs on POST /log ...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
