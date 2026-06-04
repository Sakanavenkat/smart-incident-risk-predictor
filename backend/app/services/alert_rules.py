"""Alert rule engine for ticket notifications."""
from datetime import datetime
from typing import Dict, List


class AlertRuleEngine:
    """Determines which alerts to send based on ticket risk."""

    ALERT_RULES = {
        "Critical": {
            "severity": "CRITICAL",
            "notify_immediately": True,
            "template": "critical_ticket",
            "cc_roles": ["admin", "manager"]
        },
        "High": {
            "severity": "HIGH",
            "notify_immediately": True,
            "template": "high_risk_ticket",
            "cc_roles": ["manager"]
        },
        "Medium": {
            "severity": "MEDIUM",
            "notify_immediately": False,
            "template": "medium_risk_ticket",
            "cc_roles": []
        },
        "Safe": {
            "severity": "LOW",
            "notify_immediately": False,
            "template": None,
            "cc_roles": []
        }
    }

    @staticmethod
    def should_alert(risk_label: str, sla_percentage: float) -> bool:
        """Determine if alert should be sent."""
        if risk_label in ["Critical", "High"]:
            return True
        if sla_percentage < 20:
            return True
        return False

    @staticmethod
    def get_alert_recipients(risk_label: str, assignment_group: str = None) -> Dict:
        """Get alert recipients based on risk level."""
        rule = AlertRuleEngine.ALERT_RULES.get(risk_label, {})
        return {
            "primary": f"{assignment_group}@example.com" if assignment_group else "support@example.com",
            "cc": ["manager@example.com"] if "manager" in rule.get("cc_roles", []) else [],
            "severity": rule.get("severity", "LOW"),
            "notify_immediately": rule.get("notify_immediately", False)
        }

    @staticmethod
    def compose_alert_message(ticket_data: Dict, prediction: Dict) -> Dict:
        """Compose alert email message."""
        risk_label = prediction.get("predicted_label", "Unknown")
        subject = f"[{risk_label}] Ticket {ticket_data.get('ticket_id')} - Risk Alert"
        
        body = f"""
        TICKET ALERT - {risk_label}
        
        Ticket ID: {ticket_data.get('ticket_id')}
        Priority: {ticket_data.get('priority')}
        Category: {ticket_data.get('category')}
        Open Days: {ticket_data.get('open_days')}
        SLA %: {ticket_data.get('sla_percentage')}
        
        RISK PREDICTION:
        - Label: {risk_label}
        - Confidence: {prediction.get('confidence', 0):.2%}
        - Model Version: {prediction.get('model_version')}
        
        RECOMMENDED ACTIONS:
        """
        
        if risk_label == "Critical":
            body += "\n- ESCALATE IMMEDIATELY to senior support team"
            body += "\n- Review and prioritize for SLA compliance"
            body += "\n- Consider customer impact assessment"
        elif risk_label == "High":
            body += "\n- Expedite ticket resolution"
            body += "\n- Assign to experienced support staff"
            body += "\n- Monitor SLA status closely"
        elif risk_label == "Medium":
            body += "\n- Track SLA progress"
            body += "\n- Follow up with customer if needed"
        
        body += f"\n\nAlert Generated: {datetime.utcnow().isoformat()}"
        
        return {
            "subject": subject,
            "body": body,
            "html": f"<h2>{subject}</h2><pre>{body}</pre>"
        }
