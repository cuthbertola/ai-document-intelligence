#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/Users/olawalebadekale/ai-document-platform/backend')

from app.services.ocr_service import ocr_service
from pathlib import Path

# Test with one of your upload files
test_file = "/Users/olawalebadekale/ai-document-platform/data/uploads/20250821_160753_4012FTE_2425JANMAY_Portfolio_Tasksheet_Resit (1).pdf"

if os.path.exists(test_file):
    print(f"Testing OCR on: {test_file}")
    result = ocr_service.process_document(test_file)
    
    print(f"Success: {result.success}")
    print(f"Text extracted: {len(result.text)} characters")
    print(f"Confidence: {result.confidence}")
    print(f"Text file path: {result.metadata.get('text_file_path', 'Not saved')}")
    print(f"Metadata file path: {result.metadata.get('metadata_file_path', 'Not saved')}")
    
    # Check if files were created
    processed_dir = Path("/Users/olawalebadekale/ai-document-platform/data/processed")
    base_name = Path(test_file).stem
    
    txt_file = processed_dir / f"{base_name}.txt"
    json_file = processed_dir / f"{base_name}_metadata.json"
    
    print(f"\nChecking for output files:")
    print(f"Text file exists: {txt_file.exists()} - {txt_file}")
    print(f"JSON file exists: {json_file.exists()} - {json_file}")
    
    # Also check uploads folder
    uploads_dir = Path("/Users/olawalebadekale/ai-document-platform/data/uploads")
    txt_file_uploads = uploads_dir / f"{base_name}.txt"
    json_file_uploads = uploads_dir / f"{base_name}_metadata.json"
    
    print(f"\nChecking uploads folder:")
    print(f"Text file in uploads: {txt_file_uploads.exists()} - {txt_file_uploads}")
    print(f"JSON file in uploads: {json_file_uploads.exists()} - {json_file_uploads}")
else:
    print(f"Test file not found: {test_file}")
