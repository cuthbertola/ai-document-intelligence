from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import os
import json
from datetime import datetime
from app.core.config import settings
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db
from app.api.routers import ocr, process

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)
app.include_router(process.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Document Intelligence Platform", "version": settings.APP_VERSION, "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    from app.models.document import Document
    
    contents = await file.read()
    file_size = len(contents)
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, safe_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    
    # Save to database
    db_document = Document(
        filename=safe_filename,
        file_type=os.path.splitext(file.filename)[1].replace(".", ""),
        file_size=file_size,
        status="uploaded",
        original_path=file_path
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "message": "File uploaded successfully",
        "filename": safe_filename,
        "size": file_size,
        "status": "uploaded",
        "document_id": db_document.id
    }

def get_document_by_id(document_id: int):
    try:
        upload_folder = settings.UPLOAD_FOLDER
        processed_folder = os.path.join(os.path.dirname(settings.UPLOAD_FOLDER), "processed")
        all_documents = []
        
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    all_documents.append({
                        "id": len(all_documents) + 1,
                        "filename": filename,
                        "file_path": file_path,
                        "size": stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(stat.st_ctime),
                        "status": "uploaded",
                        "file_type": os.path.splitext(filename)[1],
                        "document_type": "Uploaded",
                        "folder": "uploads"
                    })
        
        if os.path.exists(processed_folder):
            for filename in os.listdir(processed_folder):
                if filename.endswith("_metadata.json"):
                    continue
                file_path = os.path.join(processed_folder, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    ext = os.path.splitext(filename)[1]
                    display_name = f"OCR_{filename[:8]}...{ext}"
                    all_documents.append({
                        "id": len(all_documents) + 1,
                        "filename": display_name,
                        "original_filename": filename,
                        "file_path": file_path,
                        "size": stat.st_size,
                        "uploaded_at": datetime.fromtimestamp(stat.st_ctime),
                        "status": "completed",
                        "file_type": ext,
                        "document_type": "OCR Processed",
                        "folder": "processed"
                    })
        
        if document_id <= 0 or document_id > len(all_documents):
            return None
        return all_documents[document_id - 1]
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.get("/api/v1/documents")
def list_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all documents from database"""
    from app.models.document import Document
    try:
        # Get documents from database
        documents = db.query(Document).order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
        total = db.query(Document).count()
        
        # Convert to response format
        doc_list = []
        for doc in documents:
            doc_list.append({
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "status": doc.status,
                "document_type": doc.document_type or "Unknown",
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "uploaded_at": doc.created_at.isoformat() if doc.created_at else None,
                "confidence": doc.confidence_score
            })
        
        return {"documents": doc_list, "total": total, "skip": skip, "limit": limit}
    except Exception as e:
        print(f"Error listing documents: {e}")
        return {"documents": [], "total": 0, "skip": skip, "limit": limit}
def list_documents(skip: int = 0, limit: int = 100):
    try:
        all_documents = []
        upload_folder = settings.UPLOAD_FOLDER
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    all_documents.append({
                        "id": len(all_documents) + 1,
                        "filename": filename,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "uploaded_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "status": "uploaded",
                        "file_type": os.path.splitext(filename)[1].replace(".", ""),
                        "document_type": "Uploaded"
                    })
        
        processed_folder = os.path.join(os.path.dirname(settings.UPLOAD_FOLDER), "processed")
        if os.path.exists(processed_folder):
            for filename in os.listdir(processed_folder):
                if filename.endswith("_metadata.json"):
                    continue
                file_path = os.path.join(processed_folder, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    ext = os.path.splitext(filename)[1]
                    display_name = f"OCR_{filename[:8]}...{ext}"
                    all_documents.append({
                        "id": len(all_documents) + 1,
                        "filename": display_name,
                        "original_filename": filename,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "uploaded_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "status": "completed",
                        "file_type": ext.replace(".", ""),
                        "document_type": "OCR Processed"
                    })
        
        all_documents.sort(key=lambda x: x["uploaded_at"], reverse=True)
        return {"documents": all_documents[skip:skip+limit], "total": len(all_documents), "skip": skip, "limit": limit}
    except Exception as e:
        print(f"Error: {e}")
        return {"documents": [], "total": 0, "skip": skip, "limit": limit}


@app.get("/api/v1/documents/{document_id}")
def get_document_details(document_id: int, db: Session = Depends(get_db)):
    """Get document details including extracted text"""
    from app.models.document import Document
    import os
    
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Calculate file size
        file_size = "Unknown"
        if document.original_path and os.path.exists(document.original_path):
            size_bytes = os.path.getsize(document.original_path)
            file_size = f"{size_bytes / (1024*1024):.1f} MB"
        
        # Get word count
        word_count = 0
        if document.extracted_text:
            word_count = len(document.extracted_text.split())
        
        return {
            "id": document.id,
            "filename": document.filename,
            "extracted_text": document.extracted_text or "No text extracted yet.",
            "word_count": word_count,
            "confidence": document.confidence_score or 0,
            "processing_time": 2.3,
            "file_size": file_size,
            "metadata": {
                "document_type": document.document_type or "Unknown",
                "pages": 0,
                "created_at": document.created_at.isoformat() if document.created_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/documents/export/excel")
def export_documents_excel(db: Session = Depends(get_db)):
    """Export all documents to Excel"""
    from app.models.document import Document
    from app.services.export_service import get_export_service
    from fastapi.responses import Response
    
    try:
        documents = db.query(Document).all()
        doc_list = []
        for doc in documents:
            doc_list.append({
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "status": doc.status,
                "confidence": doc.confidence_score,
                "document_type": doc.document_type or "Unknown",
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "word_count": len(doc.extracted_text.split()) if doc.extracted_text else 0,
                "extracted_text": doc.extracted_text or ""
            })
        
        export_service = get_export_service()
        excel_data = export_service.export_to_excel(doc_list)
        
        return Response(
            content=excel_data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=documents.xlsx"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/documents/export/csv")
def export_documents_csv(db: Session = Depends(get_db)):
    """Export all documents to CSV"""
    from app.models.document import Document
    from app.services.export_service import get_export_service
    from fastapi.responses import Response
    
    try:
        documents = db.query(Document).all()
        doc_list = []
        for doc in documents:
            doc_list.append({
                "id": doc.id,
                "filename": doc.filename,
                "file_type": doc.file_type,
                "status": doc.status,
                "confidence": doc.confidence_score,
                "document_type": doc.document_type or "Unknown",
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "word_count": len(doc.extracted_text.split()) if doc.extracted_text else 0,
                "extracted_text": doc.extracted_text or ""
            })
        
        export_service = get_export_service()
        csv_data = export_service.export_to_csv(doc_list)
        
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=documents.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    from app.models.document import Document
    import os
    
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete physical files if they exist
        if document.original_path and os.path.exists(document.original_path):
            os.remove(document.original_path)
        
        if document.processed_path and os.path.exists(document.processed_path):
            os.remove(document.processed_path)
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return {"message": "Document deleted successfully", "document_id": document_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/documents/{document_id}/entities")
def get_document_entities(document_id: int, db: Session = Depends(get_db)):
    from app.models.document import Document
    from app.services.ner_service import get_ner_service
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        if not document.extracted_text:
            return {"entities": {"persons": [], "organizations": [], "dates": [], "money": [], "locations": []}}
        ner_service = get_ner_service()
        entities = ner_service.extract_entities(document.extracted_text)
        return {"document_id": document_id, "entities": entities}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
