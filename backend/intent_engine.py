def calculate_intent(features):
    # Calculates the Shadow Intent Score (SIS) scaled 0.0 to 1.0
    
    score = (
        (0.25 * min(features["failed_connection_ratio"], 1.0)) +
        (0.20 * min(features["new_dest_ip_attempts"] / 50.0, 1.0)) +
        (0.25 * min(features["port_diversity"] / 100.0, 1.0)) +
        (0.15 * min(features["short_session_frequency"], 1.0)) +
        (0.15 * min(features["suspicious_dns_queries"] / 10.0, 1.0))
    )
    score = min(max(score, 0.0), 1.0)
    
    # Risk Level Classification
    if score >= 0.70:
        status = "High Risk"
    elif score >= 0.40:
        status = "Suspicious"
    elif score >= 0.20:
        status = "Monitor"
    else:
        status = "Safe"
        
    evidence = []
    recommended_action = []
    
    # Generate evidence based on features
    if features["failed_connection_ratio"] > 0.4:
        evidence.append(f"High failed connection ratio ({features['failed_connection_ratio']:.0%} failure rate)")
    if features["new_dest_ip_attempts"] > 10:
        evidence.append("New internal/external IP probing behavior detected")
    if features["port_diversity"] > 20:
        evidence.append(f"Unusual port scanning observed ({int(features['port_diversity'])}+ diverse ports)")
    if features["short_session_frequency"] > 0.5:
        evidence.append("Large volume of short-lived sessions (half-open/SYN packets)")
    if features["suspicious_dns_queries"] > 0:
        evidence.append(f"{int(features['suspicious_dns_queries'])} suspicious or rare DNS queries observed")
        
    # Generate recommendations based on risk
    if status == "High Risk":
        recommended_action.append("Immediately isolate device from internal network")
        recommended_action.append("Investigate device activity and inspect packet captures")
    elif status == "Suspicious":
        recommended_action.append("Investigate device activity")
        recommended_action.append("Monitor closely for escalation")
    elif status == "Monitor":
        recommended_action.append("Log detailed device traffic for baseline anomaly detection")
    else:
        recommended_action.append("No immediate action required")
        
    if not evidence:
         evidence.append("Normal baseline behavior")
         
    return score, status, evidence, recommended_action
