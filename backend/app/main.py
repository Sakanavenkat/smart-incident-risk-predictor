from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.routes import auth, tickets, users, dashboard, predictions, alerts, reports
from backend.app.db.session import engine, SessionLocal
from backend.app import models
from backend.app.utils.seed_db import init_database

app = FastAPI(
    title="Smart Incident Risk Predictor API",
    description="API for ticket risk prediction and alert management",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(predictions.router, prefix="/api", tags=["predictions"])
app.include_router(alerts.router, prefix="/api", tags=["alerts"])
app.include_router(reports.router, prefix="/api", tags=["reports"])


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Seed initial data
    db = SessionLocal()
    try:
        init_database(db)
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "smart-incident-risk",
        "docs": "/docs",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
