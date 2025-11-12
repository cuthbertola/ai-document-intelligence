from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import os
import json
from datetime import datetime
from app.core.config import settings
from app.api.routers import ocr

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Document Intelligence Platform", "version": settings.APP_VERSION, "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/v1/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    file_size = len(contents)
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_FOLDER, safe_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    return {"message": "File uploaded successfully", "filename": safe_filename, "size": file_size, "status": "uploaded"}

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

@app.post("/api/v1/process/{document_id}")
async def process_document_ocr(document_id: int):
    return {"document_id": document_id, "status": "completed", "message": "Document processed"}
