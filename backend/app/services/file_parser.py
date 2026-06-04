"""File parsing utilities for CSV and XLSX files."""
import io
import pandas as pd
from typing import Tuple, List, Dict


class FileParser:
    """Parse CSV and XLSX files."""

    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
    REQUIRED_COLUMNS = {
        "ticket_id", "priority", "category", "region",
        "assignment_group", "open_date", "sla_percentage", "status"
    }

    @staticmethod
    def validate_file_extension(filename: str) -> Tuple[bool, str]:
        """Validate file extension."""
        import os
        _, ext = os.path.splitext(filename.lower())
        if ext not in FileParser.ALLOWED_EXTENSIONS:
            return False, f"File extension {ext} not supported. Use .csv or .xlsx"
        return True, ""

    @staticmethod
    def parse_file(file_content: bytes, filename: str) -> Tuple[bool, pd.DataFrame | None, str]:
        """
        Parse CSV or XLSX file.
        
        Returns:
            (success: bool, dataframe: pd.DataFrame | None, error_message: str)
        """
        try:
            if filename.lower().endswith(".csv"):
                df = pd.read_csv(io.BytesIO(file_content))
            elif filename.lower().endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                return False, None, "Unsupported file format"

            return True, df, ""
        except Exception as e:
            return False, None, f"Failed to parse file: {str(e)}"

    @staticmethod
    def validate_columns(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that all required columns are present.
        
        Returns:
            (is_valid: bool, missing_columns: List[str])
        """
        missing = FileParser.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            return False, list(missing)
        return True, []

    @staticmethod
    def validate_data_types(df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate data types of required columns.
        
        Returns:
            (is_valid: bool, error_messages: List[str])
        """
        errors = []

        # Check priority is valid
        valid_priorities = {"P1", "P2", "P3", "P4", "P5"}
        if "priority" in df.columns:
            invalid_priorities = df[~df["priority"].isin(valid_priorities)]
            if len(invalid_priorities) > 0:
                errors.append(
                    f"Invalid priorities in {len(invalid_priorities)} rows. "
                    f"Valid values: {valid_priorities}"
                )

        # Check sla_percentage is numeric
        if "sla_percentage" in df.columns:
            try:
                pd.to_numeric(df["sla_percentage"], errors="coerce")
            except:
                errors.append("sla_percentage must be numeric")

        # Check open_date is datetime
        if "open_date" in df.columns:
            try:
                pd.to_datetime(df["open_date"], errors="coerce")
            except:
                errors.append("open_date must be a valid date")

        return len(errors) == 0, errors

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize data."""
        df = df.copy()

        # Strip whitespace from string columns
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.strip()

        # Convert open_date to datetime
        if "open_date" in df.columns:
            df["open_date"] = pd.to_datetime(df["open_date"], errors="coerce")

        # Convert sla_percentage to float
        if "sla_percentage" in df.columns:
            df["sla_percentage"] = pd.to_numeric(df["sla_percentage"], errors="coerce")

        return df
