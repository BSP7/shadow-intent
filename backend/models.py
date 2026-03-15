from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DeviceLog(BaseModel):
    device_id: str
    failed_connection_ratio: float
    new_dest_ip_attempts: int
    port_diversity: int
    short_session_frequency: float
    suspicious_dns_queries: int
    timestamp: datetime

class IntentResult(BaseModel):
    device_id: str
    score: float
    status: str
    evidence: List[str]
    recommended_action: List[str]
    last_updated: datetime
