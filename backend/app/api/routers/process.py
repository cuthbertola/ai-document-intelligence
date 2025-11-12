from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.document import Document
from app.services.tesseract_ocr_service import get_tesseract_service
from app.services.document_classifier import get_classifier
from app.services.ner_service import get_ner_service
import json
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["process"])
PROCESSED_DIR = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

@router.post("/process/{document_id}")
async def process_document(document_id: int, db: Session = Depends(get_db)):
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        if document.status == "completed":
            return JSONResponse({"status": "success", "message": "Already processed", "document_id": document_id})
        document.status = "processing"
        db.commit()
        if not document.original_path or not Path(document.original_path).exists():
            document.status = "failed"
            db.commit()
            raise HTTPException(status_code=404, detail="File not found")
        
        pdf_path = Path(document.original_path)
        
        # OCR Processing
        ocr_service = get_tesseract_service()
        result = ocr_service.process_document(pdf_path)
        text = result["text"]
        page_count = result["page_count"]
        confidence = result["confidence"]
        word_count = result["word_count"]
        
        # Document Classification
        classifier = get_classifier()
        classification = classifier.classify(text)
        doc_type = classification["category"]
        classification_confidence = classification["confidence"]
        
        # Named Entity Recognition
        ner_service = get_ner_service()
        entities = ner_service.extract_entities(text)
        
        # Save extracted text
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        txt_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        # Update database
        document.extracted_text = text
        document.status = "completed"
        document.processed_path = str(txt_path)
        document.confidence_score = confidence
        document.document_type = doc_type
        document.updated_at = datetime.now()
        db.commit()
        
        return JSONResponse({
            "status": "success",
            "document_id": document_id,
            "word_count": word_count,
            "page_count": page_count,
            "confidence": confidence,
            "document_type": doc_type,
            "classification_confidence": classification_confidence,
            "method": "tesseract"
        })
    except HTTPException:
        raise
    except Exception as e:
        try:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                doc.status = "failed"
                db.commit()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))
