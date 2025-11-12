#!/usr/bin/env python3
import os
import json
from pathlib import Path

# Simple PDF text extraction without cv2
import pypdf
import pdfplumber

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pypdf or pdfplumber"""
    text = ""
    
    # Try pdfplumber first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text, "pdfplumber"
    except:
        pass
    
    # Fallback to pypdf
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text, "pypdf"
    except:
        pass
    
    return "", "failed"

# Process PDFs in uploads folder
uploads_dir = Path("/Users/olawalebadekale/ai-document-platform/data/uploads")
processed_dir = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

pdf_files = list(uploads_dir.glob("*.pdf"))
print(f"Found {len(pdf_files)} PDFs to process\n")

for pdf_file in pdf_files:
    print(f"Processing: {pdf_file.name}")
    
    text, method = extract_pdf_text(pdf_file)
    
    if text:
        # Save text file
        txt_file = processed_dir / f"{pdf_file.stem}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save metadata
        metadata = {
            "original_file": str(pdf_file),
            "text_file": str(txt_file),
            "word_count": len(text.split()),
            "char_count": len(text),
            "method": method,
            "confidence": 100.0 if method != "failed" else 0.0
        }
        
        metadata_file = processed_dir / f"{pdf_file.stem}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"  ✅ Extracted {len(text.split())} words using {method}")
        print(f"  📄 Saved to: {txt_file.name}")
        print(f"  📋 Metadata: {metadata_file.name}")
    else:
        print(f"  ❌ No text extracted")
    
    print()

# Check results
txt_files = list(processed_dir.glob("*.txt"))
json_files = list(processed_dir.glob("*_metadata.json"))
print(f"\n✅ Complete!")
print(f"📄 Text files: {len(txt_files)}")
print(f"📋 Metadata files: {len(json_files)}")
