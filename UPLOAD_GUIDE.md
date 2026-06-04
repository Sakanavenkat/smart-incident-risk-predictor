# Ticket Upload Guide

## Overview

The Smart Incident Risk Predictor allows bulk import of tickets from CSV or XLSX files. This guide covers file format, validation rules, and how to upload tickets.

---

## File Format

### Supported Formats
- CSV (.csv)
- Excel (.xlsx, .xls)

### Required Columns

All of the following columns must be present in your file:

| Column | Data Type | Description | Valid Values |
|--------|-----------|-------------|--------------|
| `ticket_id` | Text | Unique ticket identifier | Any non-empty string (e.g., T001, TICKET-123) |
| `priority` | Text | Ticket priority level | P1, P2, P3, P4, P5 |
| `category` | Text | Ticket category | Any text (e.g., Network, Database, Application) |
| `region` | Text | Geographic region | Any text (e.g., US-East, EU-Central, Asia-Pacific) |
| `assignment_group` | Text | Support team or group | Any text (e.g., Network-Support, DB-Team) |
| `open_date` | Date | When ticket was opened | ISO format: YYYY-MM-DD (e.g., 2024-01-15) |
| `sla_percentage` | Number | Current SLA percentage | 0-100 (numeric, e.g., 75.5) |
| `status` | Text | Ticket status | Any text (e.g., Open, Closed, In Progress) |

---

## Example File

### CSV Format
```csv
ticket_id,priority,category,region,assignment_group,open_date,sla_percentage,status
T001,P1,Network,US-East,Network-Support,2024-01-15,45.5,Open
T002,P2,Database,US-West,DB-Support,2024-01-20,75.3,In Progress
T003,P3,Application,EU-Central,App-Support,2024-01-10,85.0,Closed
```

### Excel Format
Same columns in the first row, with data in rows below.

**Sample file:** `ml/data/sample_tickets.csv` (included in repo)

---

## Validation Rules

When uploading a file, the system validates:

### Column Validation
- ❌ All 8 required columns must be present
- ❌ Column names are case-sensitive

### Data Validation
1. **ticket_id**: Cannot be empty
2. **priority**: Must be exactly P1, P2, P3, P4, or P5
3. **sla_percentage**: 
   - Must be numeric
   - Must be between 0 and 100
4. **open_date**: 
   - Must be valid date format (YYYY-MM-DD)
   - Cannot be in the future
5. **All other fields**: Cannot be empty

### Processing Rules
- Whitespace is trimmed from text fields
- Dates are automatically parsed
- Duplicate ticket_ids are skipped (not re-inserted)
- Invalid rows are reported but don't block the entire upload

---

## Upload Process

### Step 1: Prepare Your File

Ensure your file:
1. Contains all 8 required columns
2. Has headers in the first row
3. Is in CSV or XLSX format
4. Is less than 10MB (recommended)

### Step 2: Upload via API

#### Using curl
```bash
curl -X POST "http://localhost:8000/api/tickets/upload" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@tickets.csv"
```

#### Using Python
```python
import requests

with open("tickets.csv", "rb") as f:
    files = {"file": f}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "http://localhost:8000/api/tickets/upload",
        files=files,
        headers=headers
    )
    print(response.json())
```

#### Using FastAPI Docs
1. Navigate to http://localhost:8000/docs
2. Click **Authorize** and enter your token
3. Find the **POST /api/tickets/upload** endpoint
4. Click **Try it out**
5. Click **Choose File** and select your CSV/XLSX
6. Click **Execute**

### Step 3: Review Response

The upload endpoint returns:

```json
{
  "upload_id": 1,
  "filename": "tickets.csv",
  "total_rows": 20,
  "valid_rows": 19,
  "invalid_rows": 1,
  "success": false,
  "message": "Successfully imported 19 tickets (1 rows with errors)",
  "invalid_rows_detail": [
    {
      "row_number": 5,
      "error": "Row 5: Invalid priority 'P6'",
      "data": { "ticket_id": "T005", ... }
    }
  ]
}
```

---

## Common Errors & Solutions

### "Missing required columns"
**Cause:** One or more required columns are missing from the file.
**Solution:** Check column names match exactly (case-sensitive):
```
ticket_id, priority, category, region, assignment_group, open_date, sla_percentage, status
```

### "Invalid priority 'P6'"
**Cause:** Priority value is not P1-P5.
**Solution:** Use only valid priority levels: P1, P2, P3, P4, P5

### "sla_percentage must be numeric"
**Cause:** SLA percentage contains non-numeric data.
**Solution:** Ensure column contains only numbers (0-100).

Example:
- ✓ 75.5
- ✗ "75.5%" (remove % symbol)
- ✗ "high" (use numeric value)

### "Invalid date format in open_date"
**Cause:** Date is in wrong format.
**Solution:** Use ISO format: YYYY-MM-DD
- ✓ 2024-01-15
- ✗ 01/15/2024
- ✗ Jan 15, 2024

### "File extension .docx not supported"
**Cause:** Wrong file format.
**Solution:** Save file as CSV or XLSX only.

---

## Best Practices

1. **Validate Before Upload**
   - Open file in Excel/LibreOffice
   - Check for missing values
   - Verify date formats
   - Spot check priority values

2. **Test with Sample Data**
   - Use `ml/data/sample_tickets.csv` as a template
   - Upload sample first to verify format
   - Fix any errors in template

3. **Handle Large Files**
   - Split files >1000 rows into chunks
   - Upload incrementally
   - Monitor import logs

4. **Document Changes**
   - Record what was uploaded and when
   - Keep copy of uploaded file
   - Note any rows that failed

5. **Version Control**
   - Keep clean master copy
   - Document any data transformations
   - Track data lineage

---

## Upload History

View all past uploads via API:

```bash
curl -X GET "http://localhost:8000/api/tickets/upload-history/" \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "total": 5,
  "skip": 0,
  "limit": 50,
  "items": [
    {
      "id": 1,
      "filename": "tickets.csv",
      "total_rows": 20,
      "valid_rows": 19,
      "invalid_rows": 1,
      "errors": "[{\"row\": 5, \"error\": \"Invalid priority 'P6'\", ...}]",
      "created_at": "2024-01-25T10:30:00"
    }
  ]
}
```

---

## Performance Notes

- **Typical speed:** ~1000 tickets/second
- **Timeout:** 30 seconds per upload
- **Max file size:** Determined by server (default 10MB)
- **Batch processing:** Tickets inserted in single transaction (all or nothing)

---

## Next Steps

1. ✓ Prepare your ticket CSV/XLSX file
2. ✓ Get JWT token via login
3. ✓ Upload file using API endpoint
4. ✓ Review upload summary
5. → View tickets in Dashboard (Phase 4)
6. → Run predictions on imported tickets (Phase 4)

---

## Support

For issues:
1. Check **Common Errors & Solutions** above
2. Review **Validation Rules**
3. Validate your data file manually
4. Check FastAPI docs at http://localhost:8000/docs

---

## Sample Data for Testing

A sample file is provided at: `ml/data/sample_tickets.csv`

To use it:
```bash
curl -X POST "http://localhost:8000/api/tickets/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@ml/data/sample_tickets.csv"
```

This will import 20 sample tickets for testing dashboards and predictions.
