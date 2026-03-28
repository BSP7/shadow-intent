# Tracks metrics for model evaluation in hackathon demo
from datetime import datetime

class EvaluationMetrics:
    def __init__(self):
        self.total_evaluated = 0
        self.true_positives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.false_negatives = 0
    
    def log_prediction(self, is_actually_malicious: bool, status: str):
        self.total_evaluated += 1
        
        is_predicted_malicious = status in ["HIGH_RISK", "SUSPICIOUS"]
        
        if is_actually_malicious and is_predicted_malicious:
            self.true_positives += 1
        elif not is_actually_malicious and not is_predicted_malicious:
            self.true_negatives += 1
        elif is_actually_malicious and not is_predicted_malicious:
            self.false_negatives += 1
        elif not is_actually_malicious and is_predicted_malicious:
            self.false_positives += 1

    def get_metrics(self):
        # Calculate Rates
        detection_rate = 0.0
        if (self.true_positives + self.false_negatives) > 0:
            detection_rate = self.true_positives / (self.true_positives + self.false_negatives)
            
        false_positive_rate = 0.0
        if (self.false_positives + self.true_negatives) > 0:
            false_positive_rate = self.false_positives / (self.false_positives + self.true_negatives)
            
        accuracy = 0.0
        if self.total_evaluated > 0:
            accuracy = (self.true_positives + self.true_negatives) / self.total_evaluated
            
        return {
            "total_evaluated": self.total_evaluated,
            "anomaly_detection_rate": round(detection_rate * 100, 2), # TPR / Recall
            "false_positive_rate": round(false_positive_rate * 100, 2), 
            "accuracy": round(accuracy * 100, 2),
            "raw_counts": {
                "TP": self.true_positives,
                "FP": self.false_positives,
                "TN": self.true_negatives,
                "FN": self.false_negatives
            }
        }

# Global singleton
metrics_tracker = EvaluationMetrics()
