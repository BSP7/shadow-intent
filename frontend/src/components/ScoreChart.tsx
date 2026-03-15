import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { Device } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  devices: Device[];
}

const ScoreChart: React.FC<Props> = ({ devices }) => {
  // Sort devices or just show top 10
  const data = {
    labels: devices.map(d => d.device_id),
    datasets: [
      {
        label: 'Intent Score',
        data: devices.map(d => d.score),
        backgroundColor: devices.map(d => 
          d.score >= 0.70 ? 'rgba(220, 38, 38, 0.8)' :  // High Risk (Red)
          d.score >= 0.40 ? 'rgba(234, 88, 12, 0.8)' :  // Suspicious (Orange)
          d.score >= 0.20 ? 'rgba(234, 179, 8, 0.8)' :  // Monitor (Yellow)
          'rgba(22, 163, 74, 0.8)'                      // Safe (Green)
        ),
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: 'Real-Time Intent Scores' },
    },
    scales: {
        y: {
            min: 0,
            max: 1.0
        }
    }
  };

  return <Bar options={options} data={data} />;
};

export default ScoreChart;
