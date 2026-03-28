from datetime import datetime

# In-memory log of actions taken
action_logs = []

def simulate_mitigation(device_id: str, status: str, reason: str):
    """
    Simulates defending the network by blocking highly risky devices.
    Returns True if an action was simulated, False otherwise.
    """
    if status == "HIGH_RISK":
        action_detail = f"Firewall Rule added: DROP ALL traffic from MAC {device_id}"
        
        log_entry = {
            "device_id": device_id,
            "action": "BLOCK_DEVICE",
            "detail": action_detail,
            "reason": reason,
            "timestamp": datetime.utcnow()
        }
        
        action_logs.append(log_entry)
        print(f"\n[RESPONSE SIMULATED] -> Blocking {device_id}")
        print(f"   Reason: {reason}")
        print(f"   Detail: {action_detail}\n")
        
        return log_entry
        
    return None

def get_action_logs():
    return action_logs
