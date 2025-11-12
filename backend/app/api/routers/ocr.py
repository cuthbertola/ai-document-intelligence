from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import uuid
import logging
import PyPDF2
import json
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ocr", tags=["OCR"])

PROCESSED_DIR = Path("/Users/olawalebadekale/ai-document-platform/data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path: Path):
    """Extract text from PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {page_num + 1} ---\n{page_text}\n"
                    
        # If no text was extracted, return a message
        if not text.strip():
            text = "No text content found in PDF. The document may contain only images."
            
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        text = f"Error extracting text: {str(e)}"
        
    word_count = len(text.split())
    return text, word_count

@router.post("/process")
async def process_document(file: UploadFile = File(...)):
    """Process a PDF document and extract text."""
    
    logger.info(f"Processing file: {file.filename}")
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique ID for this document
        file_id = str(uuid.uuid4())
        pdf_filename = f"{file_id}.pdf"
        pdf_path = PROCESSED_DIR / pdf_filename
        
        # Save uploaded file
        with open(pdf_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Saved PDF to: {pdf_path}")
        
        # Extract text from PDF
        extracted_text, word_count = extract_text_from_pdf(pdf_path)
        
        # Save extracted text
        txt_filename = f"{file_id}.txt"
        txt_path = PROCESSED_DIR / txt_filename
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
            
        logger.info(f"Saved text to: {txt_path}, {word_count} words")
        
        # Save metadata
        metadata = {
            "filename": pdf_filename,
            "original_filename": file.filename,
            "file_id": file_id,
            "processed_at": datetime.now().isoformat(),
            "word_count": word_count,
            "text_length": len(extracted_text)
        }
        
        metadata_path = PROCESSED_DIR / f"{file_id}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return JSONResponse({
            "status": "success",
            "file_id": file_id,
            "filename": file.filename,
            "word_count": word_count,
            "extracted_text": extracted_text,
            "message": f"Document processed successfully. {word_count} words extracted."
        })
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "processed_dir": str(PROCESSED_DIR),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/document/{document_id}")
async def get_document_text(document_id: str):
    """Get extracted text for a document."""
    
    txt_path = PROCESSED_DIR / f"{document_id}.txt"
    
    if not txt_path.exists():
        raise HTTPException(status_code=404, detail="Text file not found")
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    return {
        "text": text,
        "word_count": len(text.split()),
        "document_id": document_id
    }
