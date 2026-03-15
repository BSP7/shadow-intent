import React from 'react';
import { Alert } from '../types';

interface Props {
  alerts: Alert[];
}

const AlertPanel: React.FC<Props> = ({ alerts }) => {
  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '16px',
      height: '80vh',
      overflowY: 'auto',
      backgroundColor: '#fff0f0'
    }}>
      <h2>Security Alerts</h2>
      {alerts.length === 0 ? (
        <p>No active alerts.</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {alerts.map((alert, idx) => (
            <li key={idx} style={{
              padding: '10px',
              borderBottom: '1px solid #ddd',
              backgroundColor: '#fff',
              marginBottom: '5px'
            }}>
              <strong>{alert.device_id}</strong>
              <div style={{ color: 'red', fontWeight: 'bold' }}>{alert.message}</div>
              <small>{new Date(alert.timestamp).toLocaleString()}</small>
              
              {alert.evidence && alert.evidence.length > 0 && (
                <div style={{ fontSize: '0.85em', marginTop: '8px' }}>
                  <strong>Evidence:</strong>
                  <ul style={{ paddingLeft: '20px', margin: '4px 0' }}>
                    {alert.evidence.map((e, i) => <li key={i}>{e}</li>)}
                  </ul>
                </div>
              )}
              
              {alert.recommended_action && alert.recommended_action.length > 0 && (
                <div style={{ fontSize: '0.85em', marginTop: '8px' }}>
                  <strong>Recommended Action:</strong>
                  <ul style={{ paddingLeft: '20px', margin: '4px 0' }}>
                    {alert.recommended_action.map((a, i) => <li key={i}>{a}</li>)}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AlertPanel;
