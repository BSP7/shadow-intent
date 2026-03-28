from sklearn.ensemble import IsolationForest
import numpy as np
from database import get_db

# Connect to database via get_db
db = get_db()
baselines_collection = db["baselines"]

# Cache models per device
_models = {}

def update_baseline(device_id, features: dict):
    """Store historical device behavior in MongoDB"""
    feature_vector = [
        features.get("port_variance", 0.0),
        features.get("packet_rate", 0.0),
        features.get("dns_entropy", 0.0),
        features.get("protocol_entropy", 0.0),
    ]
    
    # Store in MongoDB
    baselines_collection.update_one(
        {"device_id": device_id},
        {"$push": {
            "history": {
                "$each": [feature_vector],
                "$slice": -500  # Keep last 500 records
            }
        }},
        upsert=True
    )
    
    # Retrain model periodically when data comes in
    train_model(device_id)

def get_baseline(device_id):
    """Fetch average baseline for simple heuristic fallback"""
    record = baselines_collection.find_one({"device_id": device_id})
    if not record or not record.get("history"):
        return [0, 0, 0, 0]
    
    history = np.array(record["history"])
    return np.mean(history, axis=0).tolist()

def train_model(device_id):
    """Train Isolation Forest on normal baseline data"""
    record = baselines_collection.find_one({"device_id": device_id})
    if not record or len(record.get("history", [])) < 10:
        return False # Not enough data
    
    X = np.array(record["history"])
    clf = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    clf.fit(X)
    _models[device_id] = clf
    return True

def get_ml_anomaly_score(device_id, current_features: dict) -> float:
    """Detect anomalies in real-time. Outputs 0 (normal) to 1 (highly anomalous)."""
    if device_id not in _models:
        success = train_model(device_id)
        if not success:
            return 0.0 # Fallback 0
            
    clf = _models[device_id]
    
    current_vector = [
        current_features.get("port_variance", 0.0),
        current_features.get("packet_rate", 0.0),
        current_features.get("dns_entropy", 0.0),
        current_features.get("protocol_entropy", 0.0),
    ]
    
    # decision_function outputs values where lower/negative are anomalies.
    score = clf.decision_function([current_vector])[0]
    
    # Convert to 0-1 scale: 0 = Normal, 1 = Max Anomaly
    # Score is roughly between -0.5 to 0.5. Invert it.
    normalized_score = 0.5 - max(min(score, 0.5), -0.5)
    
    return normalized_score

def calculate_deviation(current_features: dict, baseline: list) -> float:
    if not baseline or sum(baseline) == 0:
        return 0.0
    current_vector = [
        current_features.get("port_variance", 0.0),
        current_features.get("packet_rate", 0.0),
        current_features.get("dns_entropy", 0.0),
        current_features.get("protocol_entropy", 0.0),
    ]
    deviation = np.linalg.norm(np.array(current_vector) - np.array(baseline))
    return min(deviation / 100.0, 1.0)
