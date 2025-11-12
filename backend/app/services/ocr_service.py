from pathlib import Path
import PyPDF2
from typing import NamedTuple, Dict, Any
from enum import Enum

class DocumentType(Enum):
    PDF = "pdf"
    TEXT = "text"
    IMAGE = "image"
    UNKNOWN = "unknown"

class OCRResult(NamedTuple):
    success: bool
    text: str
    confidence: float
    metadata: Dict[str, Any]
    document_type: DocumentType

class OCRService:
    def process_document(self, file_path: str, use_advanced: bool = False) -> OCRResult:
        """Process a document and extract text."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return OCRResult(
                    success=False,
                    text="",
                    confidence=0.0,
                    metadata={"error": "File not found"},
                    document_type=DocumentType.UNKNOWN
                )
            
            # Extract text from PDF
            if path.suffix.lower() == '.pdf':
                text = self._extract_pdf_text(path)
                word_count = len(text.split())
                
                # Save extracted text to a .txt file
                txt_path = path.with_suffix('.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                return OCRResult(
                    success=True,
                    text=text,
                    confidence=95.5 if word_count > 100 else 75.0,
                    metadata={
                        "word_count": word_count,
                        "char_count": len(text),
                        "classification": "Document",
                        "text_file": str(txt_path)
                    },
                    document_type=DocumentType.PDF
                )
            
            # For text files, just read them
            elif path.suffix.lower() == '.txt':
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                return OCRResult(
                    success=True,
                    text=text,
                    confidence=100.0,
                    metadata={
                        "word_count": len(text.split()),
                        "char_count": len(text)
                    },
                    document_type=DocumentType.TEXT
                )
            
            return OCRResult(
                success=False,
                text="",
                confidence=0.0,
                metadata={"error": "Unsupported file type"},
                document_type=DocumentType.UNKNOWN
            )
            
        except Exception as e:
            return OCRResult(
                success=False,
                text="",
                confidence=0.0,
                metadata={"error": str(e)},
                document_type=DocumentType.UNKNOWN
            )
    
    def _extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {page_num + 1} ---\n{page_text}\n"
        except Exception as e:
            text = f"Error extracting text: {e}"
        
        if not text.strip():
            text = "No readable text found in PDF. The document may contain only images."
        
        return text.strip()

# Create singleton instance
ocr_service = OCRService()
