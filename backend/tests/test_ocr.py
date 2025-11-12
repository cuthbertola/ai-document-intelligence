"""
Test suite for OCR functionality.
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.services.ocr_service import ocr_service

# Create test client - FIXED: Use proper initialization
client = TestClient(app)

# Test files directory
TEST_FILES_DIR = Path(__file__).parent / "test_files"
TEST_FILES_DIR.mkdir(exist_ok=True)

def test_ocr_service_initialization():
    """Test OCR service initializes correctly"""
    assert ocr_service is not None
    assert ocr_service.tesseract_config == '--oem 3 --psm 6'

def test_process_text_file():
    """Test text file processing"""
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

def test_ocr_health_check():
    """Test OCR service health check endpoint"""
    response = client.get("/api/ocr/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ocr_available" in data
    assert data["ocr_available"] == True

def test_api_extract_text():
    """Test quick text extraction endpoint"""
    test_content = "Quick extraction test content"
    test_file_path = TEST_FILES_DIR / "test_extract.txt"
    
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    # Test extraction
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/ocr/extract-text",
            files={"file": ("test_extract.txt", f, "text/plain")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == test_content
    assert data["confidence"] == 100.0
    assert data["word_count"] == len(test_content.split())
    
    # Cleanup
    if test_file_path.exists():
        test_file_path.unlink()

def test_unsupported_file_type():
    """Test handling of unsupported file types"""
    test_file_path = TEST_FILES_DIR / "test.xyz"
    
    with open(test_file_path, 'w') as f:
        f.write("unsupported content")
    
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/ocr/process",
            files={"file": ("test.xyz", f, "application/octet-stream")}
        )
    
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]
    
    # Cleanup
    if test_file_path.exists():
        test_file_path.unlink()

# Cleanup function to ensure test files directory is clean
def cleanup_test_files():
    """Clean up any remaining test files"""
    if TEST_FILES_DIR.exists():
        for file in TEST_FILES_DIR.glob("*"):
            if file.is_file():
                file.unlink()

# Run cleanup after all tests
def teardown_module(module):
    """Clean up after all tests in this module"""
    cleanup_test_files()