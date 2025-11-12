import os
from pathlib import Path
import PyPDF2
import json
from datetime import datetime

# Set the correct processed folder path
PROCESSED_DIR = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyPDF2."""
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
            
            # If still no text, try OCR (if available)
            if len(text.strip()) < 100:
                try:
                    import pytesseract
                    from pdf2image import convert_from_path
                    
                    print(f"    Low text ({len(text.strip())} chars), attempting OCR...")
                    images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=min(3, num_pages))
                    
                    for i, image in enumerate(images):
                        ocr_text = pytesseract.image_to_string(image)
                        text += f"\n--- OCR Page {i+1} ---\n{ocr_text}"
                except Exception as ocr_error:
                    print(f"    OCR failed: {ocr_error}")
    
    except Exception as e:
        print(f"    Error extracting text: {e}")
        return None
    
    return text

def process_all_pdfs():
    """Process all PDFs in the folder."""
    pdf_files = list(PROCESSED_DIR.glob("*.pdf"))
    
    # Filter out metadata files
    pdf_files = [pdf for pdf in pdf_files if "_metadata" not in pdf.stem]
    
    print(f"📁 Processing folder: {PROCESSED_DIR}")
    print(f"📊 Found {len(pdf_files)} PDF files to check")
    print("=" * 60)
    
    processed = 0
    updated = 0
    failed = 0
    skipped = 0
    
    for idx, pdf_path in enumerate(pdf_files, 1):
        txt_path = pdf_path.with_suffix('.txt')
        metadata_path = pdf_path.parent / f"{pdf_path.stem}_metadata.json"
        
        print(f"\n[{idx}/{len(pdf_files)}] 📄 {pdf_path.name}")
        
        # Check if .txt file exists and has content
        needs_processing = False
        if not txt_path.exists():
            print(f"    ⚠️  Missing .txt file")
            needs_processing = True
        else:
            with open(txt_path, 'r', encoding='utf-8') as f:
                existing_text = f.read()
            
            if len(existing_text.strip()) < 100:
                print(f"    ⚠️  Low content in existing .txt ({len(existing_text.strip())} chars)")
                needs_processing = True
            else:
                print(f"    ✓ Existing .txt has {len(existing_text.strip())} characters")
                skipped += 1
        
        if needs_processing:
            print(f"    🔄 Extracting text...")
            extracted_text = extract_text_from_pdf(pdf_path)
            
            if extracted_text and len(extracted_text.strip()) > 50:
                # Save text file
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                
                word_count = len(extracted_text.split())
                char_count = len(extracted_text)
                
                print(f"    ✅ Saved {txt_path.name}")
                print(f"       Characters: {char_count}, Words: {word_count}")
                
                if txt_path.exists():
                    updated += 1
                else:
                    processed += 1
                
                # Create or update metadata
                metadata = {
                    "filename": pdf_path.name,
                    "file_id": pdf_path.stem,
                    "processed_at": datetime.now().isoformat(),
                    "text_length": char_count,
                    "word_count": word_count,
                    "extraction_method": "PyPDF2" if char_count > 100 else "PyPDF2+OCR"
                }
                
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                print(f"    ✅ Updated metadata")
            else:
                print(f"    ❌ Failed to extract meaningful text")
                failed += 1
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"  ✅ Newly processed: {processed}")
    print(f"  🔄 Updated: {updated}")
    print(f"  ⏭️  Skipped (already good): {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📁 Total PDFs: {len(pdf_files)}")
    print(f"  📄 Total TXT files: {len(list(PROCESSED_DIR.glob('*.txt')))}")

if __name__ == "__main__":
    print("🚀 Processing all PDFs in the processed folder...")
    print("This may take a few minutes depending on the number of files...\n")
    process_all_pdfs()
    print("\n✅ Processing complete!")
