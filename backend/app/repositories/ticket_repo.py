"""Ticket repository for database operations."""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from backend.app import models, schemas


class TicketRepository:
    """Ticket data access layer."""

    @staticmethod
    def create_ticket(db: Session, ticket_data: dict) -> models.Ticket:
        """Create a single ticket."""
        # Calculate open_days
        open_date = ticket_data.get("open_date")
        open_days = (datetime.utcnow().date() - open_date.date()).days if open_date else 0

        db_ticket = models.Ticket(
            ticket_id=ticket_data["ticket_id"],
            priority=ticket_data["priority"],
            category=ticket_data["category"],
            region=ticket_data["region"],
            assignment_group=ticket_data["assignment_group"],
            open_date=open_date,
            sla_percentage=ticket_data["sla_percentage"],
            status=ticket_data["status"],
            open_days=open_days,
        )
        db.add(db_ticket)
        return db_ticket

    @staticmethod
    def create_bulk_tickets(db: Session, tickets_data: List[dict]) -> int:
        """Create multiple tickets in bulk."""
        created_count = 0
        for ticket_data in tickets_data:
            try:
                TicketRepository.create_ticket(db, ticket_data)
                created_count += 1
            except Exception:
                # Skip on duplicate or error
                continue

        db.commit()
        return created_count

    @staticmethod
    def get_ticket_by_id(db: Session, ticket_id: int) -> models.Ticket | None:
        """Get ticket by database ID."""
        return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    @staticmethod
    def get_ticket_by_ticket_id(db: Session, ticket_id: str) -> models.Ticket | None:
        """Get ticket by ticket_id (unique identifier)."""
        return db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()

    @staticmethod
    def get_all_tickets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        priority: str | None = None,
        region: str | None = None,
        assignment_group: str | None = None,
        status: str | None = None
    ) -> tuple[List[models.Ticket], int]:
        """Get tickets with filtering and pagination."""
        query = db.query(models.Ticket)

        if priority:
            query = query.filter(models.Ticket.priority == priority)
        if region:
            query = query.filter(models.Ticket.region == region)
        if assignment_group:
            query = query.filter(models.Ticket.assignment_group == assignment_group)
        if status:
            query = query.filter(models.Ticket.status == status)

        total = query.count()
        tickets = query.offset(skip).limit(limit).all()
        return tickets, total

    @staticmethod
    def update_ticket(db: Session, ticket_id: int, update_data: dict) -> models.Ticket | None:
        """Update a ticket."""
        db_ticket = TicketRepository.get_ticket_by_id(db, ticket_id)
        if not db_ticket:
            return None

        for key, value in update_data.items():
            if hasattr(db_ticket, key):
                setattr(db_ticket, key, value)

        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def delete_ticket(db: Session, ticket_id: int) -> bool:
        """Delete a ticket."""
        db_ticket = TicketRepository.get_ticket_by_id(db, ticket_id)
        if not db_ticket:
            return False

        db.delete(db_ticket)
        db.commit()
        return True

    @staticmethod
    def count_tickets(db: Session) -> int:
        """Count total tickets."""
        return db.query(models.Ticket).count()


class UploadHistoryRepository:
    """Upload history data access layer."""

    @staticmethod
    def create_upload(
        db: Session,
        filename: str,
        uploaded_by: int,
        total_rows: int,
        valid_rows: int,
        invalid_rows: int,
        errors: str = ""
    ) -> models.UploadHistory:
        """Create upload history record."""
        db_upload = models.UploadHistory(
            filename=filename,
            uploaded_by=uploaded_by,
            total_rows=total_rows,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            errors=errors,
        )
        db.add(db_upload)
        db.commit()
        db.refresh(db_upload)
        return db_upload

    @staticmethod
    def get_upload_history(db: Session, skip: int = 0, limit: int = 50) -> tuple[List[models.UploadHistory], int]:
        """Get upload history with pagination."""
        query = db.query(models.UploadHistory)
        total = query.count()
        uploads = query.order_by(models.UploadHistory.created_at.desc()).offset(skip).limit(limit).all()
        return uploads, total

    @staticmethod
    def get_upload_by_id(db: Session, upload_id: int) -> models.UploadHistory | None:
        """Get specific upload by ID."""
        return db.query(models.UploadHistory).filter(models.UploadHistory.id == upload_id).first()
