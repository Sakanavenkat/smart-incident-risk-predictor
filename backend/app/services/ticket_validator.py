"""Ticket validation and processing logic."""
import pandas as pd
from datetime import datetime
from typing import List, Tuple, Dict


class TicketValidator:
    """Validate ticket data before storing."""

    @staticmethod
    def validate_row(row: pd.Series, row_index: int) -> Tuple[bool, str | None]:
        """
        Validate a single ticket row.
        
        Returns:
            (is_valid: bool, error_message: str | None)
        """
        # Check required fields
        required_fields = ["ticket_id", "priority", "category", "region",
                          "assignment_group", "open_date", "sla_percentage", "status"]

        for field in required_fields:
            if field not in row or pd.isna(row[field]):
                return False, f"Row {row_index + 2}: Missing required field '{field}'"

        # Validate ticket_id is non-empty
        if not str(row["ticket_id"]).strip():
            return False, f"Row {row_index + 2}: ticket_id cannot be empty"

        # Validate priority
        valid_priorities = {"P1", "P2", "P3", "P4", "P5"}
        if str(row["priority"]).strip() not in valid_priorities:
            return False, f"Row {row_index + 2}: Invalid priority '{row['priority']}'"

        # Validate sla_percentage is numeric and between 0-100
        try:
            sla = float(row["sla_percentage"])
            if sla < 0 or sla > 100:
                return False, f"Row {row_index + 2}: SLA percentage must be between 0-100"
        except (ValueError, TypeError):
            return False, f"Row {row_index + 2}: sla_percentage must be numeric"

        # Validate open_date
        try:
            if isinstance(row["open_date"], str):
                datetime.fromisoformat(row["open_date"])
            # If already datetime object, it's valid
        except (ValueError, TypeError):
            return False, f"Row {row_index + 2}: Invalid date format in open_date"

        return True, None

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> Tuple[List[Dict], List[Dict]]:
        """
        Validate entire dataframe and separate valid/invalid rows.
        
        Returns:
            (valid_rows: List[Dict], invalid_rows: List[Dict])
        """
        valid_rows = []
        invalid_rows = []

        for idx, row in df.iterrows():
            is_valid, error = TicketValidator.validate_row(row, idx)
            if is_valid:
                valid_rows.append(row.to_dict())
            else:
                invalid_rows.append({
                    "row_number": idx + 2,
                    "data": row.to_dict(),
                    "error": error
                })

        return valid_rows, invalid_rows

    @staticmethod
    def prepare_for_storage(row: Dict) -> Dict:
        """Prepare a validated row for database storage."""
        prepared = {
            "ticket_id": str(row["ticket_id"]).strip(),
            "priority": str(row["priority"]).strip(),
            "category": str(row["category"]).strip(),
            "region": str(row["region"]).strip(),
            "assignment_group": str(row["assignment_group"]).strip(),
            "open_date": pd.to_datetime(row["open_date"]),
            "sla_percentage": float(row["sla_percentage"]),
            "status": str(row["status"]).strip(),
        }
        return prepared
