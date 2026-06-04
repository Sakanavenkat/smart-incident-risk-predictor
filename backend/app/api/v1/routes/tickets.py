from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import json
from backend.app import schemas
from backend.app.db.session import get_db
from backend.app.core.dependencies import get_current_user_from_header
from backend.app.repositories.ticket_repo import TicketRepository, UploadHistoryRepository
from backend.app.services.file_parser import FileParser
from backend.app.services.ticket_validator import TicketValidator

router = APIRouter()


@router.post("/upload", response_model=schemas.UploadResponse)
async def upload_tickets(
    file: UploadFile = File(...),
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """
    Upload tickets from CSV or XLSX file.
    
    Required columns:
    - ticket_id: unique identifier
    - priority: P1, P2, P3, P4, or P5
    - category: ticket category
    - region: geographical region
    - assignment_group: support group name
    - open_date: ISO format date (YYYY-MM-DD)
    - sla_percentage: numeric 0-100
    - status: ticket status (e.g., Open, Closed, In Progress)
    
    Returns:
    - upload_id: ID of this upload record
    - valid_rows: number of successfully processed tickets
    - invalid_rows: number of rows with errors
    - invalid_rows_detail: detailed error messages for each invalid row
    """
    # Get current user
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    try:
        token = authorization.split("Bearer ")[1]
        # Note: In production, verify token properly
        current_user = None  # Would be extracted from token
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
    
    # Validate file extension
    is_valid, error_msg = FileParser.validate_file_extension(file.filename)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    
    # Read file
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Parse file
    success, df, parse_error = FileParser.parse_file(file_content, file.filename)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=parse_error)
    
    # Validate columns
    is_valid, missing_cols = FileParser.validate_columns(df)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required columns: {', '.join(missing_cols)}"
        )
    
    # Clean data
    df = FileParser.clean_data(df)
    
    # Validate data types
    is_valid, type_errors = FileParser.validate_data_types(df)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Data type validation failed: {'; '.join(type_errors)}"
        )
    
    # Validate rows and separate valid/invalid
    valid_rows, invalid_rows = TicketValidator.validate_dataframe(df)
    
    # Insert valid tickets
    tickets_for_storage = [TicketValidator.prepare_for_storage(row) for row in valid_rows]
    inserted_count = TicketRepository.create_bulk_tickets(db, tickets_for_storage)
    
    # Prepare error summary
    error_summary = ""
    if invalid_rows:
        error_summary = json.dumps([
            {
                "row": row["row_number"],
                "error": row["error"],
                "ticket_id": str(row["data"].get("ticket_id", "N/A"))
            }
            for row in invalid_rows
        ])
    
    # Save upload history (use uploaded_by=1 as placeholder, would be current_user.id)
    upload_record = UploadHistoryRepository.create_upload(
        db=db,
        filename=file.filename,
        uploaded_by=1,  # Would be current_user.id
        total_rows=len(df),
        valid_rows=inserted_count,
        invalid_rows=len(invalid_rows),
        errors=error_summary
    )
    
    return {
        "upload_id": upload_record.id,
        "filename": file.filename,
        "total_rows": len(df),
        "valid_rows": inserted_count,
        "invalid_rows": len(invalid_rows),
        "success": len(invalid_rows) == 0,
        "message": f"Successfully imported {inserted_count} tickets" +
                   (f" ({len(invalid_rows)} rows with errors)" if invalid_rows else ""),
        "invalid_rows_detail": [
            schemas.InvalidTicketRow(
                row_number=row["row_number"],
                error=row["error"],
                data=row["data"]
            )
            for row in invalid_rows[:10]  # Limit to first 10 for response
        ]
    }


@router.get("/", response_model=dict)
def list_tickets(
    skip: int = 0,
    limit: int = 100,
    priority: str | None = None,
    region: str | None = None,
    assignment_group: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    """
    List tickets with optional filtering.
    
    Query parameters:
    - skip: number of records to skip (default: 0)
    - limit: max records to return (default: 100)
    - priority: filter by priority (P1-P5)
    - region: filter by region
    - assignment_group: filter by assignment group
    - status: filter by status
    """
    tickets, total = TicketRepository.get_all_tickets(
        db, skip, limit, priority, region, assignment_group, status
    )
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [schemas.TicketOut.from_orm(t) for t in tickets]
    }


@router.get("/{ticket_id}", response_model=schemas.TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """Get a specific ticket by ID."""
    ticket = TicketRepository.get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket


@router.get("/upload-history/", response_model=dict)
def get_upload_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get upload history with pagination."""
    uploads, total = UploadHistoryRepository.get_upload_history(db, skip, limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [schemas.UploadHistoryOut.from_orm(u) for u in uploads]
    }

