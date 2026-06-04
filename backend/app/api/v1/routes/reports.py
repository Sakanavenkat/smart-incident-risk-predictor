"""Report generation API endpoints."""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services.report_generator import ReportGenerator
from typing import Dict

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily-summary", response_model=Dict)
def get_daily_summary(db: Session = Depends(get_db)):
    """Get daily incident summary."""
    return ReportGenerator.generate_daily_summary(db)


@router.get("/high-risk", response_model=Dict)
def get_high_risk_report(db: Session = Depends(get_db)):
    """Get high-risk tickets report."""
    return ReportGenerator.generate_risk_report(db)


@router.get("/export-csv")
def export_csv(db: Session = Depends(get_db)):
    """Export all tickets to CSV."""
    csv_data = ReportGenerator.export_to_csv(db)
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="tickets_export.csv"'}
    )


@router.get("/export-excel")
def export_excel(db: Session = Depends(get_db)):
    """Export all tickets to Excel."""
    excel_data = ReportGenerator.export_to_excel(db)
    return StreamingResponse(
        iter([excel_data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="tickets_export.xlsx"'}
    )
