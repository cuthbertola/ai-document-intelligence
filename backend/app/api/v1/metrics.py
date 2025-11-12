"""
Metrics API for dashboard.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.document import Document
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/metrics/overview")
def get_overview_metrics(db: Session = Depends(get_db)):
    """Get overview metrics for dashboard."""
    
    total_documents = db.query(Document).count()
    
    # Status breakdown
    status_counts = db.query(
        Document.status,
        func.count(Document.id)
    ).group_by(Document.status).all()
    
    # Document type breakdown
    type_counts = db.query(
        Document.document_type,
        func.count(Document.id)
    ).group_by(Document.document_type).all()
    
    # Processing success rate
    completed = db.query(Document).filter(Document.status == "completed").count()
    failed = db.query(Document).filter(Document.status == "failed").count()
    success_rate = (completed / (completed + failed) * 100) if (completed + failed) > 0 else 0
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_uploads = db.query(Document).filter(
        Document.created_at >= seven_days_ago
    ).count()
    
    return {
        "total_documents": total_documents,
        "status_breakdown": dict(status_counts),
        "document_types": dict(type_counts),
        "success_rate": round(success_rate, 2),
        "recent_uploads": recent_uploads
    }

@router.get("/metrics/processing-time")
def get_processing_time_metrics(db: Session = Depends(get_db)):
    """Get processing time statistics."""
    
    # This would require tracking start and end times
    # For now, return mock data
    return {
        "average_processing_time": 3.5,  # seconds
        "min_processing_time": 1.2,
        "max_processing_time": 8.7
    }