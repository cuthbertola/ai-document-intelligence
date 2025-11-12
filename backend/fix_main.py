# Fix main.py to exclude metadata files
with open('app/main.py', 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    new_lines.append(lines[i])
    # Add filter after "for filename in os.listdir(processed_folder):"
    if 'for filename in os.listdir(processed_folder):' in lines[i]:
        # Add the filter on the next line
        indent = ' ' * 16  # Adjust indent as needed
        new_lines.append(f'{indent}# Skip metadata JSON files\n')
        new_lines.append(f'{indent}if filename.endswith("_metadata.json"):\n')
        new_lines.append(f'{indent}    continue\n')
    i += 1

# Write back
with open('app/main.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Fixed main.py")
