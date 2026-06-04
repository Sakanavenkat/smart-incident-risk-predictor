"""Email alert service with SMTP support."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
from datetime import datetime


class EmailAlertService:
    """Send alert emails via SMTP."""

    def __init__(
        self,
        smtp_host: str = "localhost",
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        smtp_from: str = "alerts@example.com",
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_from = smtp_from
        self.use_tls = use_tls

    def send_alert_email(
        self,
        to_address: str,
        subject: str,
        body_html: str,
        cc_addresses: List[str] = None,
        bcc_addresses: List[str] = None,
        retry_count: int = 3
    ) -> Dict:
        """
        Send alert email with retry logic.
        
        Returns:
            {
                "success": bool,
                "message": str,
                "timestamp": str,
                "retry_attempts": int
            }
        """
        cc_addresses = cc_addresses or []
        bcc_addresses = bcc_addresses or []
        
        for attempt in range(retry_count):
            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = self.smtp_from
                message["To"] = to_address
                
                if cc_addresses:
                    message["Cc"] = ", ".join(cc_addresses)
                
                # Attach HTML version
                html_part = MIMEText(body_html, "html")
                message.attach(html_part)
                
                # Connect and send
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                    if self.use_tls:
                        server.starttls()
                    
                    if self.smtp_user:
                        server.login(self.smtp_user, self.smtp_password)
                    
                    all_recipients = [to_address] + cc_addresses + bcc_addresses
                    server.sendmail(self.smtp_from, all_recipients, message.as_string())
                
                return {
                    "success": True,
                    "message": f"Email sent to {to_address}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "retry_attempts": attempt
                }
            
            except Exception as e:
                if attempt == retry_count - 1:
                    return {
                        "success": False,
                        "message": f"Failed after {retry_count} attempts: {str(e)}",
                        "timestamp": datetime.utcnow().isoformat(),
                        "retry_attempts": attempt + 1
                    }
                continue

    def send_bulk_alerts(
        self,
        alerts: List[Dict]
    ) -> List[Dict]:
        """
        Send multiple alerts.
        
        Each alert dict should have:
        {
            "to": "recipient@example.com",
            "subject": "...",
            "body_html": "...",
            "cc": [...],
            "bcc": [...]
        }
        """
        results = []
        for alert in alerts:
            result = self.send_alert_email(
                to_address=alert["to"],
                subject=alert["subject"],
                body_html=alert["body_html"],
                cc_addresses=alert.get("cc", []),
                bcc_addresses=alert.get("bcc", [])
            )
            result["recipient"] = alert["to"]
            results.append(result)
        return results


def create_alert_html(
    ticket_id: str,
    risk_label: str,
    priority: str,
    category: str,
    open_days: int,
    sla_percentage: float,
    confidence: float,
    assignment_group: str,
    recommended_actions: str
) -> str:
    """Create HTML email body for alert."""
    
    risk_colors = {
        "Critical": "#d32f2f",
        "High": "#f57c00",
        "Medium": "#fbc02d",
        "Safe": "#388e3c"
    }
    
    risk_color = risk_colors.get(risk_label, "#1976d2")
    
    html = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background-color: {risk_color}; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .section {{ margin: 15px 0; }}
                .label {{ font-weight: bold; }}
                .value {{ color: #333; }}
                .action-box {{ background-color: #f5f5f5; padding: 15px; border-left: 4px solid {risk_color}; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
                .badge {{ display: inline-block; background-color: {risk_color}; color: white; padding: 5px 10px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Ticket Alert</h1>
                    <p>Risk Level: <span class="badge">{risk_label}</span></p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <span class="label">Ticket Details</span>
                        <table>
                            <tr>
                                <td><span class="label">Ticket ID:</span></td>
                                <td><span class="value">{ticket_id}</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">Priority:</span></td>
                                <td><span class="value">{priority}</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">Category:</span></td>
                                <td><span class="value">{category}</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">Assignment Group:</span></td>
                                <td><span class="value">{assignment_group}</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">Open for:</span></td>
                                <td><span class="value">{open_days} days</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">SLA %:</span></td>
                                <td><span class="value">{sla_percentage}%</span></td>
                            </tr>
                        </table>
                    </div>
                    
                    <div class="section">
                        <span class="label">Risk Prediction</span>
                        <table>
                            <tr>
                                <td><span class="label">Predicted Level:</span></td>
                                <td><span class="value">{risk_label}</span></td>
                            </tr>
                            <tr>
                                <td><span class="label">Confidence:</span></td>
                                <td><span class="value">{confidence:.1%}</span></td>
                            </tr>
                        </table>
                    </div>
                    
                    <div class="action-box">
                        <span class="label">Recommended Actions:</span>
                        <p>{recommended_actions}</p>
                    </div>
                    
                    <div class="section">
                        <p style="font-size: 12px; color: #999;">
                            This is an automated alert from the Smart Incident Risk Predictor.
                            Generated at {datetime.utcnow().isoformat()}
                        </p>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return html
