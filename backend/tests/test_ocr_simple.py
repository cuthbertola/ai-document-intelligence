"""
Simplified test suite for OCR functionality.
"""
import pytest
from pathlib import Path
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test files directory
TEST_FILES_DIR = Path(__file__).parent / "test_files"
TEST_FILES_DIR.mkdir(exist_ok=True)

def test_ocr_service_import():
    """Test that OCR service can be imported"""
    from app.services.ocr_service import ocr_service
    assert ocr_service is not None
    assert ocr_service.tesseract_config == '--oem 3 --psm 6'

def test_process_text_file():
    """Test text file processing"""
    from app.services.ocr_service import ocr_service
    
    test_text = "This is a test text file.\nIt contains multiple lines.\nFor testing OCR service."
    
    test_txt_path = TEST_FILES_DIR / "test.txt"
    with open(test_txt_path, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    # Process the text file
    result = ocr_service.process_document(str(test_txt_path))
    
    assert result is not None
    assert result.document_type.value == "text"
    assert result.success == True
    assert result.text == test_text
    assert result.confidence == 100.0
    
    # Cleanup
    if test_txt_path.exists():
        test_txt_path.unlink()

def test_document_classification():
    """Test document classification"""
    from app.services.ocr_service import ocr_service
    
    # Test invoice classification
    invoice_text = "INVOICE\nTotal Amount: $500\nPayment Due: 30 days"
    result = ocr_service.classify_document(invoice_text)
    assert result == "Invoice"
    
    # Test contract classification
    contract_text = "CONTRACT AGREEMENT\nThis agreement is between party A and party B"
    result = ocr_service.classify_document(contract_text)
    assert result == "Contract"
    
    # Test unknown classification
    unknown_text = "Random text without specific keywords"
    result = ocr_service.classify_document(unknown_text)
    assert result == "Other"
