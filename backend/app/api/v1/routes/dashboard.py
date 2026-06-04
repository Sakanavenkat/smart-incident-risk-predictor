"""Dashboard API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Get ticket summary statistics.
    
    Returns:
    - total_tickets: total number of tickets
    - open_tickets: tickets with status "Open"
    - closed_tickets: tickets with status "Closed"
    - in_progress_tickets: tickets with status "In Progress"
    - high_risk_tickets: tickets with priority P1 or P2
    - average_sla_percentage: average SLA across all tickets
    """
    return DashboardService.get_ticket_summary(db)


@router.get("/priority-distribution")
def get_priority_distribution(db: Session = Depends(get_db)):
    """Get ticket count by priority level (P1-P5)."""
    return {
        "distribution": DashboardService.get_priority_distribution(db)
    }


@router.get("/status-distribution")
def get_status_distribution(db: Session = Depends(get_db)):
    """Get ticket count by status."""
    return {
        "distribution": DashboardService.get_status_distribution(db)
    }


@router.get("/region-distribution")
def get_region_distribution(db: Session = Depends(get_db)):
    """Get ticket count by region."""
    return {
        "distribution": DashboardService.get_region_distribution(db)
    }


@router.get("/category-performance")
def get_category_performance(db: Session = Depends(get_db)):
    """
    Get performance metrics by category.
    
    Returns for each category:
    - total: total tickets in category
    - closed: closed tickets in category
    - average_sla: average SLA percentage
    - closure_rate: percentage of tickets closed
    """
    return {
        "categories": DashboardService.get_category_performance(db)
    }


@router.get("/assignment-group-workload")
def get_assignment_group_workload(db: Session = Depends(get_db)):
    """
    Get workload metrics by assignment group.
    
    Returns for each group:
    - total_tickets: total assigned tickets
    - open_tickets: open tickets in group
    - average_sla: average SLA percentage
    """
    return {
        "groups": DashboardService.get_assignment_group_workload(db)
    }


@router.get("/sla-trend")
def get_sla_trend(days: int = 7, db: Session = Depends(get_db)):
    """
    Get SLA trend over the last N days.
    
    Query parameters:
    - days: number of days to look back (default: 7)
    
    Returns:
    - date: ISO date
    - average_sla: average SLA for that day
    - ticket_count: tickets created that day
    """
    return {
        "trend": DashboardService.get_sla_trend(db, days)
    }


@router.get("/oldest-tickets")
def get_oldest_tickets(limit: int = 10, db: Session = Depends(get_db)):
    """
    Get oldest open tickets.
    
    Query parameters:
    - limit: max number of tickets to return (default: 10)
    
    Returns list of open tickets sorted by open_date (oldest first).
    """
    return {
        "tickets": DashboardService.get_oldest_tickets(db, limit)
    }


@router.get("/")
def get_full_dashboard(db: Session = Depends(get_db)):
    """
    Get complete dashboard data (all metrics).
    
    This combines:
    - summary
    - priority_distribution
    - status_distribution
    - region_distribution
    - category_performance
    - assignment_group_workload
    - sla_trend
    - oldest_tickets
    
    Use individual endpoints for better performance if you only need specific data.
    """
    return DashboardService.get_dashboard_data(db)
