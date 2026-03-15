import requests
devices = requests.get('http://localhost:8000/devices').json()
print(f'%-15s | %-10s | %-15s | %-30s' % ('Device ID','Score','Status','Primary Evidence'))
print('-'*80)
for d in devices:
    evidence = d['evidence'][0] if d.get('evidence') else 'Normal'
    if len(evidence) > 30: evidence = evidence[:27] + '...'
    print(f"{d['device_id']:<15} | {d['score']*100:5.1f}%     | {d['status']:<15} | {evidence:<30}")
