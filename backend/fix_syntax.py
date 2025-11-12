# Read main.py
with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'r') as f:
    content = f.read()

# Fix the syntax error in the f-string
content = content.replace(
    'text += f"--- Page {page_num + 1} ---',
    'text += f"--- Page {page_num + 1} ---\\n"'
)

# Write back
with open('/Users/olawalebadekale/ai-document-platform/backend/app/main.py', 'w') as f:
    f.write(content)

print("✅ Fixed syntax error")
