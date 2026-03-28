from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List, Dict, Any
from datetime import datetime

from models import DeviceLog, IntentResult
from feature_extractor import extract_features
from intent_engine import calculate_intent
from alert_engine import trigger_alert
from response_engine import simulate_mitigation, get_action_logs
from evaluation import metrics_tracker
from database import get_device_history

app = FastAPI(title="Shadow Intent System - Advanced Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory stores
device_store: Dict[str, IntentResult] = {}
alert_history: List[Dict] = []

def process_log(log: DeviceLog):
    features = extract_features(log)
    
    # 1. Intent Engine (Includes ML Baseline Check)
    score, status, triggered_features, recommended_action = calculate_intent(log.device_id, features)
    
    # 2. XAI Alert Engine
    alert_info = None
    if status in ["HIGH_RISK", "SUSPICIOUS"]:
        alert_info = trigger_alert(log.device_id, score, status, triggered_features)
        if alert_info:
            # Prevent spamming alerts
            if not alert_history or (alert_history[-1]["device_id"] != log.device_id or (datetime.utcnow() - alert_history[-1]["timestamp"]).seconds > 10):
                 alert_info["timestamp"] = datetime.utcnow()
                 alert_history.append(alert_info)
                 if len(alert_history) > 100:
                     alert_history.pop(0)

    # 3. Simulated Response
    mitigation = simulate_mitigation(log.device_id, status, alert_info["reason"] if alert_info else "Status update")

    # 4. Track Evaluation Metrics
    # (assuming attack_simulator sets features to extreme if malicious)
    is_simulated_attack = features.get("packet_rate", 0) > 400 or features.get("port_variance", 0) > 30
    metrics_tracker.log_prediction(is_actually_malicious=is_simulated_attack, status=status)
    
    # 5. Build Result
    result = IntentResult(
        device_id=log.device_id,
        score=score,
        status=status,
        evidence=triggered_features,
        recommended_action=recommended_action,
        last_updated=datetime.now()
    )
    
    device_store[log.device_id] = result
    return result

@app.get("/")
def read_root():
    return {"status": "Shadow Intent System Online", "version": "Hackathon Edition"}

@app.post("/log", response_model=IntentResult)
async def ingest_log(log: DeviceLog):
    return process_log(log)

@app.get("/devices", response_model=List[IntentResult])
async def get_devices():
    devices = list(device_store.values())
    return sorted(devices, key=lambda x: x.score, reverse=True)

@app.get("/device/{device_id}/history")
async def get_history(device_id: str):
    """Retrieve historical score and feature baselines for a specific device from MongoDB"""
    # Requires MongoDB to have data via baseline_model
    return {"history": get_device_history(device_id)}

@app.get("/alerts")
async def get_alerts():
    return alert_history[::-1]  # Return newest first

@app.get("/actions")
async def get_actions():
    return get_action_logs()[::-1]

@app.get("/metrics")
async def get_metrics():
    return metrics_tracker.get_metrics()

@app.on_event("startup")
async def startup_event():
    print("Backend ready. Modules Loaded:")
    print(" - ML Intent Engine (Isolation Forest)")
    # - Persistent Baselines
    print(" - XAI Alerts")
    print(" - Automated Mitigation Engine")
    print("Waiting for live network logs on POST /log ...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
