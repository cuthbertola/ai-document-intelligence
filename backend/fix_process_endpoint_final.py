import re

with open('app/main.py', 'r') as f:
    content = f.read()

# Replace the broken process endpoint with a working one
new_process_endpoint = '''@app.post("/api/v1/process/{document_id}")
async def process_document_ocr(document_id: int):
    """Process a document with OCR."""
    try:
        document = get_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if document.get("status") == "completed":
            raise HTTPException(status_code=400, detail="Document already processed")
        
        file_path = document["file_path"]
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Use the OCR router's process function
        from app.api.routers.ocr import process_document
        from fastapi import UploadFile
        
        # Create an UploadFile object from the existing file
        with open(file_path, 'rb') as f:
            contents = await f.read() if hasattr(f.read, '__await__') else f.read()
            
        # Create UploadFile instance
        from io import BytesIO
        import tempfile
        
        # Create a temporary file to work with
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path)[1]) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        
        # Process using the OCR router
        with open(tmp_path, 'rb') as f:
            upload_file = UploadFile(filename=document["filename"], file=f)
            result = await process_document(file=upload_file, use_advanced=False)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        if result.get("success"):
            # Move file to processed folder if it was in uploads
            if document.get("folder") == "uploads":
                processed_folder = os.path.join(os.path.dirname(settings.UPLOAD_FOLDER), "processed")
                new_path = os.path.join(processed_folder, os.path.basename(file_path))
                if not os.path.exists(new_path):
                    shutil.move(file_path, new_path)
            
            return {
                "success": True,
                "document_id": document_id,
                "filename": document["filename"],
                "message": f"Document processed successfully",
                "text_length": result.get("text_length", 0),
                "confidence": result.get("confidence", 0)
            }
        else:
            raise HTTPException(status_code=500, detail="Processing failed")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")'''

# Find and replace the process endpoint
pattern = r'@app\.post\("/api/v1/process/\{document_id\}"\)[\s\S]*?(?=\n@app\.|$)'
content = re.sub(pattern, new_process_endpoint, content, flags=re.DOTALL)

# Add required imports at the top if not present
if 'import tempfile' not in content:
    import_section = content.find('from datetime import datetime')
    if import_section != -1:
        content = content[:import_section] + 'import tempfile\n' + content[import_section:]

with open('app/main.py', 'w') as f:
    f.write(content)

print("✅ Process endpoint fixed!")
print("✅ Process button should now work from the UI")
print("The backend will reload automatically.")
