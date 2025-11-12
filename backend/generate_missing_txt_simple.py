import os
from pathlib import Path
import json
from datetime import datetime

# Set the correct processed folder path
PROCESSED_DIR = Path("/Users/olawalebadekale/ai-document-platform/data/processed")

# Check available packages
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("⚠️  PyPDF2 not available")

try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR packages not available")

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using available methods."""
    text = ""
    
    if not PYPDF2_AVAILABLE:
        print(f"  Cannot extract text - PyPDF2 not installed")
        return None
    
    try:
        # Try to extract text directly with PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # If no text extracted and OCR is available, try OCR
        if len(text.strip()) < 100 and OCR_AVAILABLE:
            print(f"  Low text content ({len(text.strip())} chars), trying OCR...")
            try:
                images = convert_from_path(pdf_path, dpi=200)
                for i, image in enumerate(images):
                    ocr_text = pytesseract.image_to_string(image)
                    text += f"\n--- Page {i+1} ---\n{ocr_text}"
            except Exception as ocr_error:
                print(f"  OCR failed: {ocr_error}")
    
    except Exception as e:
        print(f"  Error extracting text: {e}")
        return None
    
    return text

def check_processed_folder():
    """Check the status of the processed folder."""
    if not PROCESSED_DIR.exists():
        print(f"❌ Processed folder does not exist: {PROCESSED_DIR}")
        return
    
    pdf_files = list(PROCESSED_DIR.glob("*.pdf"))
    txt_files = list(PROCESSED_DIR.glob("*.txt"))
    
    print(f"📁 Processed folder: {PROCESSED_DIR}")
    print(f"📊 Found {len(pdf_files)} PDF files")
    print(f"📊 Found {len(txt_files)} TXT files")
    print("=" * 50)
    
    # Check which PDFs are missing .txt files
    missing_txt = []
    low_content = []
    
    for pdf_path in pdf_files:
        if "_metadata" in pdf_path.stem:
            continue
            
        txt_path = pdf_path.with_suffix('.txt')
        
        if not txt_path.exists():
            missing_txt.append(pdf_path)
        else:
            # Check if existing .txt file has meaningful content
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    existing_text = f.read()
                if len(existing_text.strip()) < 100:
                    low_content.append((pdf_path, len(existing_text.strip())))
            except:
                pass
    
    if missing_txt:
        print(f"\n📄 PDFs missing .txt files ({len(missing_txt)}):")
        for pdf in missing_txt[:5]:  # Show first 5
            print(f"  - {pdf.name}")
        if len(missing_txt) > 5:
            print(f"  ... and {len(missing_txt) - 5} more")
    
    if low_content:
        print(f"\n⚠️  TXT files with low content ({len(low_content)}):")
        for pdf, char_count in low_content[:5]:  # Show first 5
            print(f"  - {pdf.name}: {char_count} chars")
        if len(low_content) > 5:
            print(f"  ... and {len(low_content) - 5} more")
    
    # Try to generate missing files if packages are available
    if PYPDF2_AVAILABLE and missing_txt:
        print("\n🔧 Attempting to generate missing .txt files...")
        for pdf_path in missing_txt[:3]:  # Process first 3 as a test
            print(f"\n📄 Processing: {pdf_path.name}")
            txt_path = pdf_path.with_suffix('.txt')
            
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"  ✅ Created {txt_path.name} ({len(extracted_text)} characters)")
            else:
                print(f"  ❌ Failed to extract text")

if __name__ == "__main__":
    print("🔍 Checking processed folder and text files...")
    print("=" * 50)
    check_processed_folder()
    print("\n✅ Analysis complete")
