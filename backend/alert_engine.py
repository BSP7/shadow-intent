def classify_risk(score):
    if score >= 60:
        return "MALICIOUS"
    elif score >= 30:
        return "SUSPICIOUS"
    else:
        return "NORMAL"

def trigger_alert(device_id, score, status):
    if status == "MALICIOUS":
        print(f"ALERT: High Intent Detected on {device_id} (Score: {score:.2f})")
        # In a real system, this would send an email/SMS or webhook
