# Machine Learning & Alerts Integration Guide

## Quick Start: Phase 5 Features

### 1. Get Predictions for Uploaded Tickets

#### Single Ticket Prediction
```bash
curl -X POST http://localhost:8000/api/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T001",
    "priority": "P1",
    "category": "Network",
    "open_days": 5,
    "sla_percentage": 45.5
  }'
```

Response:
```json
{
  "ticket_id": "T001",
  "predicted_label": "Critical",
  "confidence": 0.95,
  "score": 1.0,
  "model_version": "rule_v1"
}
```

#### Batch Predictions
Predict risk for multiple tickets at once:
```bash
curl -X POST http://localhost:8000/api/predictions/predict-batch \
  -H "Content-Type: application/json" \
  -d '[
    {"ticket_id": "T001", "priority": "P1", "category": "Network", "open_days": 5, "sla_percentage": 45.5},
    {"ticket_id": "T002", "priority": "P2", "category": "Database", "open_days": 25, "sla_percentage": 30.0},
    {"ticket_id": "T003", "priority": "P3", "category": "Application", "open_days": 10, "sla_percentage": 70.0}
  ]'
```

---

### 2. Send Risk Alerts

#### Auto-Alert High-Risk Tickets
```bash
curl -X POST http://localhost:8000/api/alerts/send-alert \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T001",
    "risk_label": "Critical",
    "sla_percentage": 45.5,
    "assignment_group": "Network-Support",
    "recipient": "network-team@example.com"
  }'
```

Response:
```json
{
  "ticket_id": "T001",
  "status": "sent",
  "message": "Alert sent to network-team@example.com",
  "recipients": {
    "primary": "network-team@example.com",
    "cc": ["manager@example.com"],
    "severity": "CRITICAL",
    "notify_immediately": true
  }
}
```

#### View Alert Rules
```bash
curl -X GET http://localhost:8000/api/alerts/rules
```

---

### 3. Generate Reports

#### Daily Incident Summary
```bash
curl -X GET http://localhost:8000/api/reports/daily-summary
```

Response:
```json
{
  "date": "2024-01-25",
  "total_tickets": 45,
  "by_priority": {
    "P1": 3,
    "P2": 8,
    "P3": 20,
    "P4": 10,
    "P5": 4
  },
  "by_status": {
    "Open": 25,
    "In Progress": 10,
    "Closed": 10
  },
  "average_sla": 72.5,
  "generated_at": "2024-01-25T10:30:00.123456"
}
```

#### High-Risk Tickets Report
```bash
curl -X GET http://localhost:8000/api/reports/high-risk
```

Response:
```json
{
  "total_risk_tickets": 12,
  "critical_priority": 3,
  "low_sla": 5,
  "tickets": [
    {
      "ticket_id": "T001",
      "priority": "P1",
      "open_days": 35,
      "sla_percentage": 15.5
    },
    ...
  ],
  "generated_at": "2024-01-25T10:30:00.123456"
}
```

#### Export to CSV
```bash
curl -X GET http://localhost:8000/api/reports/export-csv -o tickets_export.csv
```

Opens in Excel, LibreOffice, or Google Sheets.

#### Export to Excel
```bash
curl -X GET http://localhost:8000/api/reports/export-excel -o tickets_export.xlsx
```

Full formatting with headers and columns.

---

## Risk Prediction Rules

### How Risk is Calculated

**Critical (95% confidence)**
- Priority = P1

**High (85% confidence)**
- Priority = P2, OR
- Open for > 30 days, OR
- SLA < 30%

**Medium (75% confidence)**
- SLA < 50%

**Safe (90% confidence)**
- All other cases

### Risk Score
- Safe: 0.0
- Medium: 0.33
- High: 0.66
- Critical: 1.0

---

## Alert System

### Automatic Alert Conditions

| Risk Level | Action | Recipients |
|-----------|--------|-----------|
| Critical | Send immediately | Primary + managers |
| High | Send immediately | Primary + manager |
| Medium | Log only | None |
| Safe | Log only | None |

### Example Alert Message

Subject: `[CRITICAL] Ticket T001 - Risk Alert`

Body:
```
TICKET ALERT - CRITICAL

Ticket ID: T001
Priority: P1
Category: Network
Open Days: 5
SLA %: 45.5

RISK PREDICTION:
- Label: Critical
- Confidence: 95%
- Model Version: rule_v1

RECOMMENDED ACTIONS:
- ESCALATE IMMEDIATELY to senior support team
- Review and prioritize for SLA compliance
- Consider customer impact assessment

Alert Generated: 2024-01-25T10:30:00
```

---

## Complete Workflow Example

### Step 1: Upload Tickets
```bash
curl -X POST http://localhost:8000/api/tickets/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample_tickets.csv"
```

### Step 2: Get Predictions
```bash
curl -X POST http://localhost:8000/api/predictions/predict-batch \
  -H "Content-Type: application/json" \
  -d '[
    {"ticket_id": "T001", "priority": "P1", "category": "Network", "open_days": 5, "sla_percentage": 45.5},
    {"ticket_id": "T002", "priority": "P2", "category": "Database", "open_days": 25, "sla_percentage": 30.0}
  ]'
```

### Step 3: Send Alerts for High-Risk
```bash
# For T001 (Critical)
curl -X POST http://localhost:8000/api/alerts/send-alert \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T001",
    "risk_label": "Critical",
    "sla_percentage": 45.5,
    "assignment_group": "Network-Support"
  }'

# For T002 (High)
curl -X POST http://localhost:8000/api/alerts/send-alert \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T002",
    "risk_label": "High",
    "sla_percentage": 30.0,
    "assignment_group": "DB-Support"
  }'
```

### Step 4: Generate Report
```bash
curl -X GET http://localhost:8000/api/reports/daily-summary > daily_report.json
curl -X GET http://localhost:8000/api/reports/export-csv > tickets.csv
```

---

## API Reference

### Predictions
- `POST /api/predictions/predict` - Single prediction
- `POST /api/predictions/predict-batch` - Batch predictions

### Alerts
- `POST /api/alerts/send-alert` - Send alert
- `GET /api/alerts/rules` - Get rules

### Reports
- `GET /api/reports/daily-summary` - Summary
- `GET /api/reports/high-risk` - Risk report
- `GET /api/reports/export-csv` - CSV export
- `GET /api/reports/export-excel` - Excel export

---

## Implementation Notes

### Rule-Based Prediction
Current system uses simple IF/THEN rules for speed and explainability. Perfect for MVP.

### Background Alerts
Alerts are sent in the background, so endpoint returns immediately.

### Export Formats
- CSV: Plain text, works everywhere
- Excel: Formatted with headers and colors

### Extensibility
Rules can be easily modified in `AlertRuleEngine` for custom alert logic.

---

## Troubleshooting

### Prediction Always Returns "Safe"
Check if ticket has reasonable open_days and sla_percentage values.

### Alert Not Sending
Verify `should_alert()` conditions are met - need High/Critical risk or SLA < 20%.

### CSV Export Empty
Ensure tickets have been uploaded (Phase 3) first.

---

## Next: Phase 6 - Email Alerts

Real email integration will be added in Phase 6 with:
- SMTP configuration
- Email templates
- Alert history
- Retry logic

For now, alerts are logged and ready for email service integration.
