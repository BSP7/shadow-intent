from baseline_model import get_ml_anomaly_score, update_baseline, get_baseline, calculate_deviation

def calculate_intent(device_id: str, features: dict):
    # Retrieve required features (fallback to 0 if not present)
    port_variance = features.get("port_variance", 0)
    packet_rate = features.get("packet_rate", 0)
    dns_entropy = features.get("dns_entropy", 0)
    protocol_entropy = features.get("protocol_entropy", 0)
    
    # Persistent Behavior Learning
    baseline = get_baseline(device_id)
    baseline_deviation = calculate_deviation(features, baseline)
    
    # Update baseline after calculating deviation to not bias current check
    update_baseline(device_id, features)
    
    # ML Anomaly Score (Isolation Forest)
    ml_anomaly_score = get_ml_anomaly_score(device_id, features)

    # Calculate Shadow Intent Score (0.0 to 1.0 scale)
    # Give ML score significant weight along with heuristics
    score = (
        (0.15 * min(port_variance / 100.0, 1.0)) +
        (0.15 * min(packet_rate / 1000.0, 1.0)) +
        (0.15 * min(dns_entropy, 1.0)) +
        (0.10 * min(protocol_entropy, 1.0)) +
        (0.15 * min(baseline_deviation, 1.0)) +
        (0.30 * min(ml_anomaly_score, 1.0))
    )
    score = float(min(max(score, 0.0), 1.0))
    
    # Risk Level Classification
    if score >= 0.70:
        status = "HIGH_RISK"
    elif score >= 0.40:
        status = "SUSPICIOUS"
    elif score >= 0.20:
        status = "MONITOR"
    else:
        status = "SAFE"
        
    triggered_features = []
    
    # Generate evidence based on features
    if port_variance > 20:
        triggered_features.append("High port variance (Potential scan)")
    if packet_rate > 500:
        triggered_features.append("Abnormal packet burst (Potential DoS)")
    if baseline_deviation > 0.5:
        triggered_features.append("Significant baseline deviation")
    if ml_anomaly_score > 0.6:
        triggered_features.append("ML IsolationForest Anomaly Detected")
        
    # Generate recommendations based on risk
    recommended_action = []
    if status == "HIGH_RISK":
        recommended_action.append("Immediately isolate device from internal network")
        recommended_action.append("Trigger active response to simulate blocking")
    elif status == "SUSPICIOUS":
        recommended_action.append("Investigate device activity")
        recommended_action.append("Monitor closely for escalation")
    elif status == "MONITOR":
        recommended_action.append("Log detailed device traffic for baseline anomaly detection")
    else:
        recommended_action.append("No immediate action required")
        
    if not triggered_features:
         triggered_features.append("Normal baseline behavior")
         
    return score, status, triggered_features, recommended_action
