import os
from pathlib import Path
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
import json
from datetime import datetime

# Set the correct processed folder path
PROCESSED_DIR = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyPDF2 first, then OCR if needed."""
    text = ""
    
    try:
        # First try to extract text directly
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # If no text extracted, try OCR
        if len(text.strip()) < 100:
            print(f"  Low text content ({len(text.strip())} chars), trying OCR...")
            images = convert_from_path(pdf_path, dpi=200)
            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image)
                text += f"\n--- Page {i+1} ---\n{ocr_text}"
    
    except Exception as e:
        print(f"  Error extracting text: {e}")
        return None
    
    return text

def generate_missing_txt_files():
    """Generate .txt files for PDFs that don't have them."""
    pdf_files = list(PROCESSED_DIR.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files in processed folder")
    
    for pdf_path in pdf_files:
        # Skip metadata files
        if "_metadata" in pdf_path.stem:
            continue
            
        txt_path = pdf_path.with_suffix('.txt')
        
        # Check if .txt file exists
        if not txt_path.exists():
            print(f"\n📄 Processing: {pdf_path.name}")
            print(f"  Missing .txt file, generating...")
            
            # Extract text
            extracted_text = extract_text_from_pdf(pdf_path)
            
            if extracted_text:
                # Save text file
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"  ✅ Created {txt_path.name} ({len(extracted_text)} characters)")
            else:
                print(f"  ❌ Failed to extract text")
        else:
            # Check if existing .txt file has meaningful content
            with open(txt_path, 'r', encoding='utf-8') as f:
                existing_text = f.read()
            
            if len(existing_text.strip()) < 100:
                print(f"\n📄 Re-processing: {pdf_path.name}")
                print(f"  Existing .txt has only {len(existing_text.strip())} characters")
                
                extracted_text = extract_text_from_pdf(pdf_path)
                if extracted_text and len(extracted_text.strip()) > len(existing_text.strip()):
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(extracted_text)
                    print(f"  ✅ Updated {txt_path.name} ({len(extracted_text)} characters)")

if __name__ == "__main__":
    print("🔍 Checking for missing .txt files...")
    print(f"Processed folder: {PROCESSED_DIR}")
    print("=" * 50)
    generate_missing_txt_files()
    print("\n✅ Finished processing missing text files")
