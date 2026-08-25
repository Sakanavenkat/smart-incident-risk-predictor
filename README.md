# Smart Incident Risk Predictor & Alert Management System

Monorepo scaffold for a beginner-friendly FastAPI + React application that ingests ticket CSV/XLSX files, predicts ticket risk with a Random Forest, displays a Material UI dashboard, and sends SMTP alerts for high-risk tickets.

## Quick Start

### Backend
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

### Frontend
```bash
cd frontend
npx create-react-app . --template cra-template
npm start
```

### Machine Learning
```bash
cd ml
python train.py
```

## Project Structure

- `backend/` - FastAPI application
- `frontend/` - React application
- `ml/` - Machine learning pipeline
- `.env.example` - Example environment variables

See the project plan in `/memories/session/plan.md` for full details.
