# Fix the config.py to point to the correct data folder
with open('app/core/config.py', 'r') as f:
    content = f.read()

# Replace the UPLOAD_FOLDER path to point to the correct location
old_path = 'UPLOAD_FOLDER: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "uploads")'
new_path = 'UPLOAD_FOLDER: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "uploads")'

content = content.replace(old_path, new_path)

with open('app/core/config.py', 'w') as f:
    f.write(content)

print("✅ Fixed UPLOAD_FOLDER path in config.py")
