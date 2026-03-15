import requests
import time
import os

for _ in range(3):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('====================================================')
    print('  SHADOW INTENT LIVE MONITOR (Press Ctrl+C to exit) ')
    print('====================================================')
    try:
        response = requests.get('http://localhost:8000/devices')
        devices = response.json()
        
        print(f"{'Device ID':<15} | {'Score':<10} | {'Status':<15} | {'Last Insight':<35}")
        print('-'*80)
        
        for d in devices:
            color = '\033[92m'
            if d['status'] == 'High Risk': color = '\033[91m'
            elif d['status'] == 'Suspicious': color = '\033[93m'
            elif d['status'] == 'Monitor': color = '\033[96m'
            
            reset = '\033[0m'
            score_pct = f"{d['score'] * 100:.1f}%"
            evidence = d['evidence'][0] if d['evidence'] else 'None'
            if len(evidence) > 35: evidence = evidence[:32] + '...'
            
            print(f"{color}{d['device_id']:<15} | {score_pct:<10} | {d['status']:<15} | {evidence}{reset}")
    except Exception as e:
        print('Waiting for API...')
    time.sleep(2)
