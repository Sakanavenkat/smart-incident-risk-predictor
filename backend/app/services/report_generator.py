"""Report generation service."""
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models import Ticket, Prediction


class ReportGenerator:
    """Generate various reports from ticket and prediction data."""

    @staticmethod
    def generate_daily_summary(db: Session) -> Dict:
        """Generate daily incident summary report."""
        today = datetime.utcnow().date()
        
        tickets = db.query(Ticket).filter(
            func.date(Ticket.created_at) == today
        ).all()
        
        if not tickets:
            return {"message": "No tickets created today"}
        
        total = len(tickets)
        by_priority = {}
        by_status = {}
        
        for ticket in tickets:
            by_priority[ticket.priority] = by_priority.get(ticket.priority, 0) + 1
            by_status[ticket.status] = by_status.get(ticket.status, 0) + 1
        
        avg_sla = sum(t.sla_percentage for t in tickets) / total if total > 0 else 0
        
        return {
            "date": str(today),
            "total_tickets": total,
            "by_priority": by_priority,
            "by_status": by_status,
            "average_sla": round(avg_sla, 2),
            "generated_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def generate_risk_report(db: Session) -> Dict:
        """Generate high-risk tickets report."""
        high_risk = db.query(Ticket).filter(
            Ticket.priority.in_(["P1", "P2"])
        ).all()
        
        critical_sla = db.query(Ticket).filter(
            Ticket.sla_percentage < 30
        ).all()
        
        risk_tickets = list(set([t.id for t in high_risk + critical_sla]))
        tickets = db.query(Ticket).filter(Ticket.id.in_(risk_tickets)).all() if risk_tickets else []
        
        return {
            "total_risk_tickets": len(tickets),
            "critical_priority": len([t for t in tickets if t.priority in ["P1", "P2"]]),
            "low_sla": len([t for t in tickets if t.sla_percentage < 30]),
            "tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "priority": t.priority,
                    "open_days": t.open_days,
                    "sla_percentage": t.sla_percentage
                }
                for t in tickets[:20]  # Top 20
            ],
            "generated_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def export_to_csv(db: Session, output_path: str = None) -> bytes:
        """Export all tickets to CSV."""
        tickets = db.query(Ticket).all()
        
        records = [
            {
                "ticket_id": t.ticket_id,
                "priority": t.priority,
                "category": t.category,
                "region": t.region,
                "assignment_group": t.assignment_group,
                "status": t.status,
                "open_days": t.open_days,
                "sla_percentage": t.sla_percentage,
                "created_at": t.created_at.isoformat() if t.created_at else ""
            }
            for t in tickets
        ]
        
        df = pd.DataFrame(records)
        
        if output_path:
            df.to_csv(output_path, index=False)
        
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()

    @staticmethod
    def export_to_excel(db: Session, output_path: str = None) -> bytes:
        """Export all tickets to Excel."""
        tickets = db.query(Ticket).all()
        
        records = [
            {
                "Ticket ID": t.ticket_id,
                "Priority": t.priority,
                "Category": t.category,
                "Region": t.region,
                "Assignment Group": t.assignment_group,
                "Status": t.status,
                "Open Days": t.open_days,
                "SLA %": t.sla_percentage,
                "Created": t.created_at.isoformat() if t.created_at else ""
            }
            for t in tickets
        ]
        
        df = pd.DataFrame(records)
        
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Tickets")
        
        if output_path:
            df.to_excel(output_path, index=False, sheet_name="Tickets")
        
        buffer.seek(0)
        return buffer.getvalue()
