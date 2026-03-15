import React from 'react';
import { Device } from '../types';

interface Props {
  device: Device;
}

const DeviceCard: React.FC<Props> = ({ device }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'High Risk': return '#dc2626'; // red
      case 'Suspicious': return '#ea580c'; // orange
      case 'Monitor': return '#eab308'; // yellow
      default: return '#16a34a'; // green
    }
  };

  return (
    <div style={{
      border: `2px solid ${getStatusColor(device.status)}`,
      borderRadius: '8px',
      padding: '16px',
      margin: '8px',
      backgroundColor: '#f9f9f9',
      width: '300px'
    }}>
      <h3>{device.device_id}</h3>
      <p>Score: <strong>{device.score.toFixed(2)}</strong></p>
      <p style={{ color: getStatusColor(device.status), fontWeight: 'bold' }}>
        {device.status}
      </p>
      <small>Last: {new Date(device.last_updated).toLocaleTimeString()}</small>
      
      {device.evidence && device.evidence.length > 0 && (
        <div style={{ marginTop: '10px', fontSize: '0.85em' }}>
          <strong>Evidence:</strong>
          <ul style={{ paddingLeft: '20px', margin: '5px 0' }}>
            {device.evidence.map((e, idx) => <li key={idx}>{e}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DeviceCard;
