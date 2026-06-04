"""Prediction API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services.ml_predictor import MLPredictor
from backend.app.repositories.ticket_repo import TicketRepository
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/predictions", tags=["predictions"])


class PredictionRequest(BaseModel):
    ticket_id: str
    priority: str
    category: str
    open_days: int
    sla_percentage: float


class PredictionResponse(BaseModel):
    ticket_id: str
    predicted_label: str
    confidence: float
    score: float
    model_version: str


@router.post("/predict", response_model=PredictionResponse)
def predict_ticket_risk(payload: PredictionRequest, db: Session = Depends(get_db)):
    """Predict risk for a single ticket."""
    ticket = TicketRepository.get_ticket_by_ticket_id(db, payload.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    prediction = MLPredictor.predict_risk(payload.dict())
    prediction["ticket_id"] = payload.ticket_id
    
    return prediction


@router.post("/predict-batch", response_model=List[PredictionResponse])
def predict_batch(payloads: List[PredictionRequest], db: Session = Depends(get_db)):
    """Predict risk for multiple tickets."""
    predictions = []
    for payload in payloads:
        ticket = TicketRepository.get_ticket_by_ticket_id(db, payload.ticket_id)
        if ticket:
            pred = MLPredictor.predict_risk(payload.dict())
            pred["ticket_id"] = payload.ticket_id
            predictions.append(pred)
    
    return predictions
