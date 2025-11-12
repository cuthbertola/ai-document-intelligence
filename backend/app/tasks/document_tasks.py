"""
Background tasks for document processing.
These run asynchronously so the API doesn't timeout.
"""

from celery import Task
from app.core.celery_app import celery_app
from app.services.ocr_service import ocr_service
from app.models.database import SessionLocal
from app.models.document import Document
import os

class CallbackTask(Task):
    """Base task with callbacks"""
    def on_success(self, retval, task_id, args, kwargs):
        """Success callback"""
        print(f"Task {task_id} succeeded")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Failure callback"""
        print(f"Task {task_id} failed: {exc}")

@celery_app.task(base=CallbackTask, bind=True, max_retries=3)
def process_document_task(self, document_id: int, file_path: str):
    """
    Process a document in the background.
    
    Args:
        document_id: Database ID of the document
        file_path: Path to the uploaded file
    """
    db = SessionLocal()
    
    try:
        # Get document from database
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")
        
        # Update status to processing
        document.status = "processing"
        db.commit()
        
        # Extract text using OCR service
        result = ocr_service.process_document(file_path)
        
        # Update document with results
        document.extracted_text = result["text"]
        document.status = "completed" if result["success"] else "failed"
        
        # Simple document classification based on keywords
        text_lower = result["text"].lower()
        if "invoice" in text_lower or "total amount" in text_lower:
            document.document_type = "invoice"
        elif "contract" in text_lower or "agreement" in text_lower:
            document.document_type = "contract"
        elif "resume" in text_lower or "curriculum" in text_lower:
            document.document_type = "resume"
        else:
            document.document_type = "other"
        
        db.commit()
        
        return {
            "document_id": document_id,
            "status": document.status,
            "text_length": len(result["text"]),
            "document_type": document.document_type
        }
        
    except Exception as e:
        # Update status to failed
        if document:
            document.status = "failed"
            db.commit()
        
        # Retry the task
        raise self.retry(exc=e, countdown=60)
    
    finally:
        db.close()