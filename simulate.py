import time
import random
import requests
from datetime import datetime

# Backend API URL
API_URL = "http://localhost:8000/log"

# Simulated devices
DEVICES = ["Smart_Fridge_01", "IP_Camera_X", "Thermostat_LivingRoom", "Smart_Bulb_Kitchen", "Industrial_Sensor_Node"]

def generate_normal_log(device_id):
    """Generates a log for normal operating behavior."""
    return {
        "device_id": device_id,
        "failed_connection_ratio": random.uniform(0.0, 0.05),
        "new_dest_ip_attempts": random.randint(0, 1),
        "port_diversity": random.randint(1, 3),
        "short_session_frequency": random.uniform(0.0, 0.1),
        "suspicious_dns_queries": 0,
        "timestamp": datetime.now().isoformat()
    }

def generate_malicious_log(device_id):
    """Generates a log simulating shadow intent or malicious behavior."""
    return {
        "device_id": device_id,
        "failed_connection_ratio": random.uniform(0.4, 0.9),
        "new_dest_ip_attempts": random.randint(10, 50),
        "port_diversity": random.randint(10, 100),
        "short_session_frequency": random.uniform(0.5, 0.95),
        "suspicious_dns_queries": random.randint(2, 10),
        "timestamp": datetime.now().isoformat()
    }

def run_simulation(interval=2):
    print(f"Starting simulation. Sending data to {API_URL} every {interval} seconds...")
    try:
        while True:
            for device in DEVICES:
                is_malicious = random.random() < 0.2
                
                if is_malicious:
                    log_data = generate_malicious_log(device)
                    print(f"⚠️  Sending MALICIOUS simulated data for {device}")
                else:
                    log_data = generate_normal_log(device)
                    print(f"✅ Sending NORMAL simulated data for {device}")
                
                try:
                    response = requests.post(API_URL, json=log_data)
                    if response.status_code == 200:
                        print(f"   Success: {response.json().get('status')} (Score: {response.json().get('score')})")
                    else:
                        print(f"   Failed to send data: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    print("   Error: Could not connect to backend. Is it running on http://localhost:8000 ?")
                
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    run_simulation(interval=3)
