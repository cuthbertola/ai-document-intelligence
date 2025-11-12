import re

with open('app/api/routers/ocr.py', 'r') as f:
    content = f.read()

# Fix the processed folder path
old_path = 'processed_dir = DATA_DIR / "processed"'
new_path = 'processed_dir = Path("/Users/olawalebadekale/ai-document-platform/data/processed")'

content = content.replace(old_path, new_path)

# Also fix any relative path references
content = content.replace('Path(__file__).parent.parent.parent / "data"', 
                         'Path("/Users/olawalebadekale/ai-document-platform/data")')

with open('app/api/routers/ocr.py', 'w') as f:
    f.write(content)

print("✅ Fixed OCR processed folder path")
