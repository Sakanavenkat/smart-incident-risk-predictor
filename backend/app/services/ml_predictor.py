"""Machine Learning service for ticket risk prediction."""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional


class MLPredictor:
    """Simple ML-based ticket risk predictor."""

    RISK_MAPPING = {
        "Safe": 0,
        "Medium": 1,
        "High": 2,
        "Critical": 3
    }

    @staticmethod
    def predict_risk(ticket_data: Dict) -> Dict:
        """
        Predict ticket risk based on features.
        
        Uses simple rules:
        - P1 priority → Critical
        - P2 priority → High
        - open_days > 30 → High
        - sla_percentage < 30 → High
        - sla_percentage < 50 → Medium
        - Otherwise → Safe
        """
        priority = ticket_data.get("priority", "")
        open_days = ticket_data.get("open_days", 0)
        sla_pct = ticket_data.get("sla_percentage", 100)
        
        # Rule-based prediction
        if priority == "P1":
            risk_label = "Critical"
            confidence = 0.95
        elif priority == "P2" or open_days > 30 or sla_pct < 30:
            risk_label = "High"
            confidence = 0.85
        elif sla_pct < 50:
            risk_label = "Medium"
            confidence = 0.75
        else:
            risk_label = "Safe"
            confidence = 0.90
        
        score = MLPredictor.RISK_MAPPING.get(risk_label, 0) / 3.0
        
        return {
            "predicted_label": risk_label,
            "confidence": confidence,
            "score": score,
            "model_version": "rule_v1"
        }

    @staticmethod
    def batch_predict(tickets_data: List[Dict]) -> List[Dict]:
        """Predict risk for multiple tickets."""
        predictions = []
        for ticket in tickets_data:
            pred = MLPredictor.predict_risk(ticket)
            pred["ticket_id"] = ticket.get("ticket_id")
            predictions.append(pred)
        return predictions
