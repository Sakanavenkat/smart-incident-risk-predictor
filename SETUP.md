# Project Setup & Getting Started

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- Git

## Backend Setup

### Windows

```bash
# 1. Run the automated setup script
install.bat

# OR manually:
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r backend/requirements.txt
```

### macOS/Linux

```bash
# 1. Run the automated setup script
bash install.sh

# OR manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Run Backend

### Windows
```bash
run.bat
```

### macOS/Linux
```bash
bash run.sh
```

The backend will start on `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Frontend Setup

```bash
cd frontend
npx create-react-app . --template cra-template
npm install
npm start
```

## Machine Learning Setup

```bash
cd ml

# 1. Add sample training data (CSV with 'label' column)
# Save to: ml/data/sample.csv

# 2. Train the model
python train.py

# 3. Model will be saved to ml/model.joblib
```

## Sample Training Data

Create `ml/data/sample.csv` with columns:
```
ticket_id,priority,category,region,assignment_group,open_date,sla_percentage,status,label
T001,P1,Network,US-East,Network-Support,2024-01-01,45.5,Open,Critical
T002,P2,Database,US-West,DB-Support,2024-01-02,75.3,Open,Medium
...
```

## Database

The backend uses SQLite for local development (file: `dev.db`).

Tables are automatically created on first run.

## Authentication

### Default Test Credentials

```
Email: admin@example.com
Password: password
```

⚠️ **These are placeholders! Replace with real authentication in Phase 2.**

## API Endpoints (Summary)

- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/tickets` - List tickets
- `POST /api/tickets/upload` - Upload CSV/XLSX
- `GET /health` - Health check

See `http://localhost:8000/docs` for full interactive API documentation.

## Development Workflow

### Phase 1: Authentication & Database ✓ SCAFFOLDED
- [x] Basic JWT auth endpoints
- [x] User & Role models
- [ ] Implement password hashing (bcrypt)
- [ ] Implement real user lookup
- [ ] Add role-based access control

### Phase 2: Ticket Upload
- [ ] CSV/XLSX file parser
- [ ] Validation logic
- [ ] Upload history tracking

### Phase 3: Dashboard
- [ ] Ticket list endpoints
- [ ] Dashboard metrics
- [ ] Chart data endpoints

### Phase 4: ML Integration
- [ ] Training pipeline
- [ ] Prediction endpoint
- [ ] Model versioning

### Phase 5: Alerts
- [ ] SMTP configuration
- [ ] Alert rules engine
- [ ] Email templates

### Phase 6: Reporting
- [ ] Report generation
- [ ] CSV/XLSX export

### Phase 7: Testing & Deployment
- [ ] Unit tests
- [ ] Integration tests
- [ ] Docker support

## Troubleshooting

### `ModuleNotFoundError: No module named 'fastapi'`
Make sure the virtual environment is activated:
- Windows: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

### Port 8000 already in use
Change the port in `run.bat` or `run.sh`:
```bash
uvicorn backend.app.main:app --reload --port 8001
```

### PostgreSQL connection issues
For production with PostgreSQL, update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/ticket_db
```

Then install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

## Next Steps

1. **Run the backend:**
   - Windows: `install.bat`, then `run.bat`
   - macOS/Linux: `bash install.sh`, then `bash run.sh`

2. **Test the API:**
   - Visit `http://localhost:8000/docs`
   - Try `/api/auth/login` with `admin@example.com` / `password`

3. **Continue with Phase 2:**
   - Implement ticket upload endpoint
   - Add CSV/XLSX parsing

4. **Review plan for details:**
   - See `/memories/session/plan.md` (saved during planning phase)

## Questions?

Refer to the project plan document for detailed architecture and design decisions.
