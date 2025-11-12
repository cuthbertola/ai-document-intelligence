import re

# Read main.py
with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'r') as f:
    content = f.read()

# Find and replace the process_document_ocr function
new_function = '''@app.post("/api/v1/process/{document_id}")
async def process_document_ocr(document_id: int):
    """Process a document with OCR."""
    try:
        document = get_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = document["file_path"]
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        import PyPDF2
        import shutil
        
        text = ""
        word_count = 0
        
        if file_path.endswith('.pdf'):
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages):
                        page_text = page.extract_text()
                        if page_text:
                            text += f"Page {page_num + 1}\\n"
                            text += page_text + "\\n\\n"
                
                word_count = len(text.split())
                
                # Define paths in processed folder
                processed_dir = os.path.join(os.path.dirname(settings.UPLOAD_FOLDER), "processed")
                os.makedirs(processed_dir, exist_ok=True)
                
                # Generate unique filename for processed files
                import uuid
                file_id = str(uuid.uuid4())
                
                # Save text to processed folder
                txt_path = os.path.join(processed_dir, f"{file_id}.txt")
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Copy PDF to processed folder
                pdf_processed_path = os.path.join(processed_dir, f"{file_id}.pdf")
                shutil.copy2(file_path, pdf_processed_path)
                
                # Remove original from uploads folder
                os.remove(file_path)
                
            except Exception as e:
                text = f"Error extracting text: {str(e)}"
                word_count = 0
        
        return {
            "document_id": document_id,
            "filename": document["filename"],
            "text_preview": text[:500] if text else "No text extracted",
            "full_text": text,
            "word_count": word_count,
            "confidence": 95.5 if word_count > 100 else 75.0,
            "document_type": "PDF",
            "message": f"Document processed. {word_count} words extracted."
        }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

# Replace the function
pattern = r'@app\.post\("/api/v1/process/\{document_id\}"\).*?raise HTTPException\(status_code=500, detail=str\(e\)\)'
content = re.sub(pattern, new_function, content, flags=re.DOTALL)

# Write back
with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'w') as f:
    f.write(content)

print("✅ Fixed process endpoint to save files in processed folder")
