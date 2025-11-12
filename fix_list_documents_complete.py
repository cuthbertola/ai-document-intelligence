import re

# Read the main.py file
with open('backend/app/main.py', 'r') as f:
    lines = f.readlines()

# Find and fix the list_documents function
in_processed_section = False
fixed_lines = []

for i, line in enumerate(lines):
    # Check if we're in the processed folder section
    if 'Get files from processed folder' in line:
        in_processed_section = True
    elif '@app.' in line and in_processed_section:
        in_processed_section = False
    
    # Fix commented metadata filter lines
    if in_processed_section:
        # Remove comments from the filter lines
        if '# if filename.endswith("_metadata.json"):' in line:
            line = line.replace('# if filename.endswith("_metadata.json"):', 
                              '                if filename.endswith("_metadata.json"):')
        elif '# continue' in line and i > 0 and 'metadata.json' in lines[i-1]:
            line = '                    continue\n'
    
    fixed_lines.append(line)

# Write back
with open('backend/app/main.py', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Fixed all metadata filters in list_documents function")

# Verify the fix
with open('backend/app/main.py', 'r') as f:
    content = f.read()
    if 'if filename.endswith("_metadata.json"):\n                    continue' in content:
        print("✅ Filter is now active and properly indented")
    else:
        print("⚠️  Filter might still need adjustment")
