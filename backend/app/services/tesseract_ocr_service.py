"""
Advanced OCR Service using Tesseract
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

class TesseractOCRService:
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        self.languages = ['eng']
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR"""
        from PIL import ImageEnhance
        image = image.convert('L')
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)
    
    def extract_text_from_image(self, image: Image.Image) -> Tuple[str, float]:
        """Extract text from image with confidence"""
        try:
            image = self.preprocess_image(image)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            text = pytesseract.image_to_string(image)
            confidences = [int(c) for c in data['conf'] if int(c) != -1]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            return text, avg_confidence
        except Exception as e:
            logger.error(f"OCR error: {e}")
            return "", 0.0
    
    def extract_text_from_pdf(self, pdf_path: Path) -> Dict:
        """Extract text from PDF"""
        try:
            images = convert_from_path(str(pdf_path), dpi=300)
            all_text = []
            page_confidences = []
            
            for i, image in enumerate(images, 1):
                text, confidence = self.extract_text_from_image(image)
                all_text.append(text)
                page_confidences.append(confidence)
            
            full_text = "\n\n".join(all_text)
            avg_confidence = sum(page_confidences) / len(page_confidences) if page_confidences else 0
            
            return {
                "text": full_text,
                "page_count": len(images),
                "confidence": round(avg_confidence, 2),
                "word_count": len(full_text.split()),
                "char_count": len(full_text),
                "method": "tesseract"
            }
        except Exception as e:
            logger.error(f"PDF OCR error: {e}")
            raise
    
    def process_document(self, file_path: Path) -> Dict:
        """Process any document"""
        if file_path.suffix.lower() == '.pdf':
            return self.extract_text_from_pdf(file_path)
        else:
            image = Image.open(file_path)
            text, confidence = self.extract_text_from_image(image)
            return {
                "text": text,
                "page_count": 1,
                "confidence": round(confidence, 2),
                "word_count": len(text.split()),
                "char_count": len(text),
                "method": "tesseract"
            }

_tesseract_service = None

def get_tesseract_service():
    global _tesseract_service
    if _tesseract_service is None:
        _tesseract_service = TesseractOCRService()
    return _tesseract_service
