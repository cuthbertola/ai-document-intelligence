import re

with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'r') as f:
    content = f.read()

# Replace the simple process endpoint with one that extracts text
new_process = '''@app.post("/api/v1/process/{document_id}")
async def process_document_ocr(document_id: int):
    """Process a document with OCR."""
    try:
        document = get_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = document["file_path"]
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Extract text if it's a PDF
        text = ""
        word_count = 0
        
        if file_path.endswith('.pdf'):
            import PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\\n"
                
                word_count = len(text.split())
                
                # Save text to processed folder
                processed_dir = os.path.join(os.path.dirname(settings.UPLOAD_FOLDER), "processed")
                os.makedirs(processed_dir, exist_ok=True)
                
                import uuid
                file_id = str(uuid.uuid4())
                txt_path = os.path.join(processed_dir, f"{file_id}.txt")
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Copy PDF to processed folder
                import shutil
                pdf_path = os.path.join(processed_dir, f"{file_id}.pdf")
                shutil.copy2(file_path, pdf_path)
                
            except Exception as e:
                return {"error": str(e)}
        
        return {
            "document_id": document_id,
            "status": "completed",
            "word_count": word_count,
            "message": f"Document processed. {word_count} words extracted."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

# Replace the process endpoint
content = re.sub(
    r'@app\.post\("/api/v1/process/\{document_id\}"\).*?return.*?\}',
    new_process,
    content,
    flags=re.DOTALL
)

with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'w') as f:
    f.write(content)

print("Added text extraction to process endpoint")
