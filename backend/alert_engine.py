from database import save_alert

# Explainable AI Alert Engine
def generate_xai_reason(status: str, triggered_features: list) -> str:
    if not triggered_features or triggered_features == ["Normal baseline behavior"]:
        return "Behavior is within normal historical and threshold parameters."
        
    reason_str = f"{status} behavior determined. Key factors: "
    reason_str += " + ".join(triggered_features)
    return reason_str

def trigger_alert(device_id: str, score: float, status: str, triggered_features: list):
    """Generates explainable alerts and saves them."""
    
    # Confidence score is exactly proportional to how strong the anomaly is over the threshold
    confidence_score = round(score * 100, 2)
    reason = generate_xai_reason(status, triggered_features)
    
    alert_payload = {
        "device_id": device_id,
        "score": score,
        "status": status,
        "confidence_score": confidence_score,
        "reason": reason,
        "triggered_features": triggered_features
    }
    
    if status in ["HIGH_RISK", "SUSPICIOUS"]:
        # Save to Mongo via database.py
        save_alert(device_id, message=reason, severity=status)
        print(f"[{status}] ALERT generated for {device_id} (Confidence: {confidence_score}%) - Reason: {reason}")
        
    return alert_payload
