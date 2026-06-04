"""Alert history repository."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from backend.app.models import AlertLog, Ticket


def log_alert(
    db: Session,
    ticket_id: int,
    risk_level: str,
    recipient: str,
    subject: str,
    status: str,
    message: str = None
) -> AlertLog:
    """Log an alert in the database."""
    alert = AlertLog(
        ticket_id=ticket_id,
        risk_level=risk_level,
        sent_to=recipient,
        subject=subject,
        body=message or "",
        status=status,
        created_at=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def get_alert_history(
    db: Session,
    ticket_id: int = None,
    limit: int = 100,
    offset: int = 0
) -> tuple[list, int]:
    """Get alert history with pagination."""
    query = db.query(AlertLog)
    
    if ticket_id:
        query = query.filter(AlertLog.ticket_id == ticket_id)
    
    total = query.count()
    alerts = query.order_by(AlertLog.created_at.desc()).offset(offset).limit(limit).all()
    
    return alerts, total


def get_alerts_by_risk_level(
    db: Session,
    risk_level: str,
    limit: int = 50
) -> list:
    """Get alerts filtered by risk level."""
    return db.query(AlertLog).filter(
        AlertLog.risk_level == risk_level
    ).order_by(AlertLog.created_at.desc()).limit(limit).all()


def get_failed_alerts(db: Session, limit: int = 50) -> list:
    """Get alerts that failed to send."""
    return db.query(AlertLog).filter(
        AlertLog.status == "failed"
    ).order_by(AlertLog.created_at.desc()).limit(limit).all()


def update_alert_status(
    db: Session,
    alert_id: int,
    status: str
) -> AlertLog:
    """Update alert status (e.g., retry pending -> sent)."""
    alert = db.query(AlertLog).get(alert_id)
    if alert:
        alert.status = status
        db.commit()
        db.refresh(alert)
    return alert


def get_alert_stats(db: Session) -> dict:
    """Get alert statistics."""
    total = db.query(AlertLog).count()
    by_risk = db.query(
        AlertLog.risk_level,
        func.count(AlertLog.id)
    ).group_by(AlertLog.risk_level).all()
    
    by_status = db.query(
        AlertLog.status,
        func.count(AlertLog.id)
    ).group_by(AlertLog.status).all()
    
    return {
        "total_alerts": total,
        "by_risk_level": {k: v for k, v in by_risk},
        "by_status": {k: v for k, v in by_status}
    }
