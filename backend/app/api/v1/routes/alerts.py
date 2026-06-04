"""Enhanced alerts API endpoints with email support."""
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services.alert_rules import AlertRuleEngine
from backend.app.services.email_service import EmailAlertService, create_alert_html
from backend.app.repositories.ticket_repo import TicketRepository
from backend.app.repositories.alert_history_repo import (
    log_alert, get_alert_history, get_alert_stats, get_failed_alerts
)
from pydantic import BaseModel, EmailStr
from typing import Optional, List

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Initialize email service
email_service = EmailAlertService(
    smtp_host="localhost",
    smtp_port=587,
    smtp_user="",
    smtp_password="",
    smtp_from="alerts@example.com",
    use_tls=True
)


class SendAlertRequest(BaseModel):
    ticket_id: str
    risk_label: str
    sla_percentage: float
    assignment_group: Optional[str] = None
    recipient: Optional[EmailStr] = None


class AlertResponse(BaseModel):
    ticket_id: str
    status: str
    message: str


class AlertHistoryResponse(BaseModel):
    id: int
    ticket_id: int
    risk_level: str
    sent_to: str
    subject: str
    status: str
    created_at: str

    class Config:
        orm_mode = True


def send_email_async(
    email_service: EmailAlertService,
    db: Session,
    ticket_id: int,
    to_address: str,
    subject: str,
    body_html: str,
    cc_addresses: List[str],
    risk_level: str,
    alert_id: int = None
):
    """Background task to send email and log result."""
    try:
        result = email_service.send_alert_email(
            to_address=to_address,
            subject=subject,
            body_html=body_html,
            cc_addresses=cc_addresses
        )
        
        status = "sent" if result["success"] else "failed"
        if alert_id:
            # Update existing alert log
            from backend.app.repositories.alert_history_repo import update_alert_status
            update_alert_status(db, alert_id, status)
    
    except Exception as e:
        pass  # Log silently


@router.post("/send-alert", response_model=AlertResponse)
def send_alert(
    payload: SendAlertRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Send alert for risky ticket."""
    ticket = TicketRepository.get_ticket_by_ticket_id(db, payload.ticket_id)
    if not ticket:
        return AlertResponse(
            ticket_id=payload.ticket_id,
            status="failed",
            message="Ticket not found"
        )
    
    # Check if alert should be sent
    should_alert = AlertRuleEngine.should_alert(payload.risk_label, payload.sla_percentage)
    
    if not should_alert:
        return AlertResponse(
            ticket_id=payload.ticket_id,
            status="skipped",
            message="Alert criteria not met"
        )
    
    # Get recipients
    recipients = AlertRuleEngine.get_alert_recipients(payload.risk_label, payload.assignment_group)
    to_address = payload.recipient or recipients["primary"]
    
    # Get recommended actions
    recommended_actions = "Review ticket status and update customer."
    if payload.risk_label == "Critical":
        recommended_actions = """
        • ESCALATE IMMEDIATELY to senior support team
        • Review and prioritize for SLA compliance
        • Consider customer impact assessment
        • Update ticket status within 2 hours
        """
    elif payload.risk_label == "High":
        recommended_actions = """
        • Expedite ticket resolution
        • Assign to experienced support staff
        • Monitor SLA status closely
        • Provide customer update
        """
    
    # Create HTML email
    body_html = create_alert_html(
        ticket_id=payload.ticket_id,
        risk_label=payload.risk_label,
        priority=ticket.priority,
        category=ticket.category,
        open_days=ticket.open_days,
        sla_percentage=payload.sla_percentage,
        confidence=0.9,
        assignment_group=payload.assignment_group or "Unassigned",
        recommended_actions=recommended_actions
    )
    
    subject = f"[{payload.risk_label}] Ticket {payload.ticket_id} - Risk Alert"
    
    # Log alert
    alert_log = log_alert(
        db=db,
        ticket_id=ticket.id,
        risk_level=payload.risk_label,
        recipient=to_address,
        subject=subject,
        status="queued",
        message=body_html
    )
    
    # Send email in background
    background_tasks.add_task(
        send_email_async,
        email_service,
        db,
        ticket.id,
        to_address,
        subject,
        body_html,
        recipients.get("cc", []),
        payload.risk_label,
        alert_log.id
    )
    
    return AlertResponse(
        ticket_id=payload.ticket_id,
        status="queued",
        message=f"Alert queued for {to_address}"
    )


@router.get("/history", response_model=dict)
def get_alerts(
    ticket_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get alert history."""
    ticket_db_id = None
    if ticket_id:
        ticket = TicketRepository.get_ticket_by_ticket_id(db, ticket_id)
        if ticket:
            ticket_db_id = ticket.id
    
    alerts, total = get_alert_history(db, ticket_db_id, limit, offset)
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [
            {
                "id": a.id,
                "ticket_id": a.ticket.ticket_id if a.ticket else "Unknown",
                "risk_level": a.risk_level,
                "sent_to": a.sent_to,
                "subject": a.subject,
                "status": a.status,
                "created_at": a.created_at.isoformat() if a.created_at else ""
            }
            for a in alerts
        ]
    }


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get alert statistics."""
    return get_alert_stats(db)


@router.get("/rules")
def get_alert_rules():
    """Get alert rule definitions."""
    return AlertRuleEngine.ALERT_RULES
