import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Device, Alert } from '../types';
import DeviceCard from './DeviceCard';
import AlertPanel from './AlertPanel';
import ScoreChart from './ScoreChart';

const Dashboard: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const fetchData = async () => {
    try {
        // Assuming backend runs on 8000
      const deviceRes = await axios.get('http://localhost:8000/devices');
      setDevices(deviceRes.data);
      
      const alertRes = await axios.get('http://localhost:8000/alerts');
      setAlerts(alertRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData(); // Initial fetch
    const interval = setInterval(fetchData, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Shadow Intent / Near-Action Analysis</h1>
      
      <div style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 2 }}>
          <h2>Live Device Status</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap' }}>
            {devices.map(d => (
              <DeviceCard key={d.device_id} device={d} />
            ))}
          </div>
          <div style={{ marginTop: '20px' }}>
             <ScoreChart devices={devices} />
          </div>
        </div>
        
        <div style={{ flex: 1 }}>
          <AlertPanel alerts={alerts} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
