#!/usr/bin/env python3
import os
import json
from pathlib import Path
import pypdf
import pdfplumber

def extract_pdf_text(pdf_path):
    """Extract text from PDF"""
    text = ""
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

# Process PDFs in processed folder that don't have text files yet
processed_dir = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

pdf_files = list(processed_dir.glob("*.pdf"))
print(f"Found {len(pdf_files)} PDFs in processed folder\n")

processed_count = 0
skipped_count = 0

for pdf_file in pdf_files:
    txt_file = processed_dir / f"{pdf_file.stem}.txt"
    metadata_file = processed_dir / f"{pdf_file.stem}_metadata.json"
    
    if txt_file.exists():
        print(f"Skip: {pdf_file.name} (already has text file)")
        skipped_count += 1
        continue
    
    print(f"Processing: {pdf_file.name}")
    text, method = extract_pdf_text(pdf_file)
    
    if text:
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        metadata = {
            "original_file": str(pdf_file),
            "text_file": str(txt_file),
            "word_count": len(text.split()),
            "char_count": len(text),
            "method": method,
            "confidence": 100.0
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"  ✅ Extracted {len(text.split())} words using {method}")
        processed_count += 1
    else:
        print(f"  ❌ No text extracted (might be a scanned PDF)")

print(f"\n📊 Summary:")
print(f"  ✅ Newly processed: {processed_count} PDFs")
print(f"  ⏭️  Skipped (already done): {skipped_count} PDFs")

# Final count
txt_files = list(processed_dir.glob("*.txt"))
json_files = list(processed_dir.glob("*_metadata.json"))
print(f"\n📁 Final counts:")
print(f"  📄 Total text files: {len(txt_files)}")
print(f"  📋 Total metadata files: {len(json_files)}")
