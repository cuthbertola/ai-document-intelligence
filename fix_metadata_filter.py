import re

# Read the main.py file
with open('backend/app/main.py', 'r') as f:
    content = f.read()

# Fix the metadata filter - uncomment and properly indent
content = re.sub(
    r'# if filename\.endswith\("_metadata\.json"\):\s*\n\s*# continue',
    'if filename.endswith("_metadata.json"):\n                    continue',
    content
)

# Write back
with open('backend/app/main.py', 'w') as f:
    f.write(content)

print("✅ Fixed metadata filter in list_documents function")
