"""Dashboard and analytics service."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from backend.app import models


class DashboardService:
    """Calculate dashboard metrics and analytics."""

    @staticmethod
    def get_ticket_summary(db: Session) -> dict:
        """Get summary statistics for tickets."""
        total = db.query(models.Ticket).count()
        open_count = db.query(models.Ticket).filter(models.Ticket.status == "Open").count()
        closed_count = db.query(models.Ticket).filter(models.Ticket.status == "Closed").count()
        in_progress = db.query(models.Ticket).filter(models.Ticket.status == "In Progress").count()
        
        # SLA metrics
        sla_avg = db.query(func.avg(models.Ticket.sla_percentage)).scalar() or 0
        
        # High risk: P1 or P2 tickets
        high_risk = db.query(models.Ticket).filter(
            models.Ticket.priority.in_(["P1", "P2"])
        ).count()
        
        return {
            "total_tickets": total,
            "open_tickets": open_count,
            "closed_tickets": closed_count,
            "in_progress_tickets": in_progress,
            "high_risk_tickets": high_risk,
            "average_sla_percentage": round(float(sla_avg), 2)
        }

    @staticmethod
    def get_priority_distribution(db: Session) -> dict:
        """Get ticket distribution by priority."""
        priorities = ["P1", "P2", "P3", "P4", "P5"]
        distribution = {}
        
        for priority in priorities:
            count = db.query(models.Ticket).filter(models.Ticket.priority == priority).count()
            distribution[priority] = count
        
        return distribution

    @staticmethod
    def get_status_distribution(db: Session) -> dict:
        """Get ticket distribution by status."""
        statuses = db.query(
            models.Ticket.status,
            func.count(models.Ticket.id).label("count")
        ).group_by(models.Ticket.status).all()
        
        return {status: count for status, count in statuses}

    @staticmethod
    def get_region_distribution(db: Session) -> dict:
        """Get ticket distribution by region."""
        regions = db.query(
            models.Ticket.region,
            func.count(models.Ticket.id).label("count")
        ).group_by(models.Ticket.region).all()
        
        return {region: count for region, count in regions}

    @staticmethod
    def get_sla_trend(db: Session, days: int = 7) -> list:
        """Get SLA trend over last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        trend_data = db.query(
            func.date(models.Ticket.created_at).label("date"),
            func.avg(models.Ticket.sla_percentage).label("avg_sla"),
            func.count(models.Ticket.id).label("ticket_count")
        ).filter(
            models.Ticket.created_at >= cutoff_date
        ).group_by(
            func.date(models.Ticket.created_at)
        ).order_by(
            func.date(models.Ticket.created_at)
        ).all()
        
        return [
            {
                "date": str(date),
                "average_sla": round(float(avg_sla), 2),
                "ticket_count": ticket_count
            }
            for date, avg_sla, ticket_count in trend_data
        ]

    @staticmethod
    def get_category_performance(db: Session) -> list:
        """Get performance metrics by category."""
        categories = db.query(
            models.Ticket.category,
            func.count(models.Ticket.id).label("count"),
            func.avg(models.Ticket.sla_percentage).label("avg_sla"),
            func.count(models.Ticket.id).filter(
                models.Ticket.status == "Closed"
            ).label("closed_count")
        ).group_by(models.Ticket.category).all()
        
        return [
            {
                "category": category,
                "total": count,
                "closed": closed_count,
                "average_sla": round(float(avg_sla), 2),
                "closure_rate": round((closed_count / count * 100), 1) if count > 0 else 0
            }
            for category, count, avg_sla, closed_count in categories
        ]

    @staticmethod
    def get_assignment_group_workload(db: Session) -> list:
        """Get workload by assignment group."""
        groups = db.query(
            models.Ticket.assignment_group,
            func.count(models.Ticket.id).label("total"),
            func.count(models.Ticket.id).filter(
                models.Ticket.status == "Open"
            ).label("open"),
            func.avg(models.Ticket.sla_percentage).label("avg_sla")
        ).group_by(models.Ticket.assignment_group).all()
        
        return [
            {
                "assignment_group": group,
                "total_tickets": total,
                "open_tickets": open_count,
                "average_sla": round(float(avg_sla), 2)
            }
            for group, total, open_count, avg_sla in groups
        ]

    @staticmethod
    def get_oldest_tickets(db: Session, limit: int = 10) -> list:
        """Get oldest open tickets."""
        tickets = db.query(models.Ticket).filter(
            models.Ticket.status == "Open"
        ).order_by(
            models.Ticket.open_date.asc()
        ).limit(limit).all()
        
        return [
            {
                "id": t.id,
                "ticket_id": t.ticket_id,
                "priority": t.priority,
                "category": t.category,
                "open_days": t.open_days,
                "sla_percentage": t.sla_percentage,
                "assignment_group": t.assignment_group
            }
            for t in tickets
        ]

    @staticmethod
    def get_dashboard_data(db: Session) -> dict:
        """Get complete dashboard data."""
        return {
            "summary": DashboardService.get_ticket_summary(db),
            "priority_distribution": DashboardService.get_priority_distribution(db),
            "status_distribution": DashboardService.get_status_distribution(db),
            "region_distribution": DashboardService.get_region_distribution(db),
            "category_performance": DashboardService.get_category_performance(db),
            "assignment_group_workload": DashboardService.get_assignment_group_workload(db),
            "sla_trend": DashboardService.get_sla_trend(db),
            "oldest_tickets": DashboardService.get_oldest_tickets(db, limit=5)
        }
