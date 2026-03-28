from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.shadow_intent

devices_collection = db.devices
alerts_collection = db.alerts
scores_collection = db.scores

def save_device(device_id, mac_address, initial_status="SAFE"):
    devices_collection.update_one(
        {"device_id": device_id},
        {"$set": {"mac_address": mac_address, "status": initial_status, "last_seen": datetime.utcnow()}},
        upsert=True
    )

def save_alert(device_id, message, severity):
    alert_doc = {
        "device_id": device_id,
        "message": message,
        "severity": severity,
        "timestamp": datetime.utcnow()
    }
    alerts_collection.insert_one(alert_doc)

def save_score(device_id, score, status, features=None):
    score_doc = {
        "device_id": device_id,
        "score": score,
        "status": status,
        "features": features or {},
        "timestamp": datetime.utcnow()
    }
    scores_collection.insert_one(score_doc)

def get_device_history(device_id, limit=50):
    return list(scores_collection.find({"device_id": device_id}, {"_id": 0}).sort("timestamp", -1).limit(limit))

def get_db():
    return db
