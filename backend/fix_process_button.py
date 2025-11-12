import re

with open('app/main.py', 'r') as f:
    content = f.read()

# Add a simple document registry after the imports
registry_code = '''
# Simple document registry to track IDs to file paths
document_registry = {}

def register_document(doc_id: int, file_path: str, filename: str, status: str):
    """Register a document in our simple registry"""
    document_registry[doc_id] = {
        "id": doc_id,
        "file_path": file_path,
        "filename": filename,
        "status": status
    }
    return doc_id

def get_document_from_registry(doc_id: int):
    """Get document from registry"""
    return document_registry.get(doc_id)
'''

# Insert after imports
import_end = content.find('app = FastAPI')
content = content[:import_end] + registry_code + '\n' + content[import_end:]

# Update list_documents to register documents
list_docs_pattern = r'(all_documents\.append\({[^}]+}\))'
replacement = r'''\1
                register_document(document_id, file_path, filename, "uploaded")'''

content = re.sub(list_docs_pattern, replacement, content)

# Replace the process endpoint with a working version
new_process_endpoint = '''@app.post("/api/v1/process/{document_id}")
async def process_document_ocr(document_id: int):
    """Process a document with OCR."""
    try:
        # First, refresh the registry by calling list_documents
        list_documents(skip=0, limit=100)
        
        # Get document from registry
        document = get_document_from_registry(document_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found. Please refresh the page.")
        
        if document["status"] == "completed":
            raise HTTPException(status_code=400, detail="Document already processed")
        
        file_path = document["file_path"]
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Process with OCR using the OCR router
        from app.api.routers.ocr import process_document as ocr_process
        
        # Read the file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Create a file-like object
        from io import BytesIO
        from fastapi import UploadFile
        
        file_obj = BytesIO(file_content)
        upload_file = UploadFile(
            filename=document["filename"],
            file=file_obj
        )
        
        # Process the document
        result = await ocr_process(file=upload_file, use_advanced=False)
        
        # Update registry
        document_registry[document_id]["status"] = "completed"
        
        return {
            "success": True,
            "message": f"Document {document['filename']} processed successfully",
            "document_id": result.get("document_id"),
            "text_length": result.get("text_length", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")'''

# Find and replace the process endpoint
pattern = r'@app\.post\("/api/v1/process/\{document_id\}"\)[\s\S]*?(?=@app\.|$)'
match = re.search(pattern, content)
if match:
    content = content[:match.start()] + new_process_endpoint + '\n\n' + content[match.end():]

with open('app/main.py', 'w') as f:
    f.write(content)

print("✅ Fixed process button - it should now work from the UI!")
print("The backend will reload automatically.")
