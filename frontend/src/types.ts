export interface Device {
  device_id: string;
  score: number;
  status: 'Safe' | 'Monitor' | 'Suspicious' | 'High Risk';
  evidence: string[];
  recommended_action: string[];
  last_updated: string;
}

export interface Alert {
  device_id: string;
  score: number;
  timestamp: string;
  message: string;
  evidence: string[];
  recommended_action: string[];
}
