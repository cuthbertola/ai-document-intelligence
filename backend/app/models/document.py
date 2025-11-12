"""
Document model - represents a document in our database.
Each uploaded document will create one of these records.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from app.models.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    # Primary key - unique identifier
    id = Column(Integer, primary_key=True, index=True)
    
    # Document metadata
    filename = Column(String, nullable=False)
    file_type = Column(String)  # pdf, jpg, png, etc.
    file_size = Column(Integer)  # in bytes
    
    # Processing status
    status = Column(String, default="pending")  # pending, processing, completed, failed
    
    # Storage paths
    original_path = Column(String)
    processed_path = Column(String)
    
    # Extracted content
    extracted_text = Column(Text)
    extracted_entities = Column(JSON)  # Store as JSON
    document_type = Column(String)  # invoice, contract, resume, etc.
    confidence_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # User who uploaded (we'll add authentication later)
    user_id = Column(Integer, nullable=True)