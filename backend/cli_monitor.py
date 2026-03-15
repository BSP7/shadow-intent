import requests
import time
import os
import sys

def print_live_feed():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('='*80)
    print('  SHADOW INTENT CLI MONITOR - REAL NETWORK MODE')
    print('='*80)
    try:
        response = requests.get('http://localhost:8000/devices')
        if response.status_code != 200:
            raise Exception("API down")
        
        devices = response.json()
        
        print(f"{'Device IP':<15} | {'Score':<8} | {'Status':<13} | {'Primary Evidence':<35}")
        print('-'*80)
        
        if not devices:
            print("No real network devices detected yet. Ensure the python sniffer is running.")
            
        for d in devices:
            # Color variables (ANSI escape sequences)
            color = '\033[92m' # Green roughly maps to Safe
            if d['status'] == 'High Risk': color = '\033[91m' # Red
            elif d['status'] == 'Suspicious': color = '\033[93m' # Yellow/Orange
            elif d['status'] == 'Monitor': color = '\033[96m' # Cyan
            reset = '\033[0m'
            
            score_pct = f"{d['score'] * 100:.0f}%"
            evidence = d['evidence'][0] if (d.get('evidence') and len(d['evidence']) > 0) else 'Normal baseline behavior'
            if len(evidence) > 38: evidence = evidence[:35] + '...'
            
            print(f"{color}{d['device_id']:<15} | {score_pct:<8} | {d['status']:<13} | {evidence}{reset}")
    except requests.exceptions.ConnectionError:
        print("Waiting for Backend API (http://localhost:8000)...")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == '__main__':
    print("Initializing Live Feed...")
    try:
        while True:
            print_live_feed()
            time.sleep(2.0)
    except KeyboardInterrupt:
        print("\nExiting Monitor...")
        sys.exit(0)