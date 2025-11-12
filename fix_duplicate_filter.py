# Read the main.py file
with open('backend/app/main.py', 'r') as f:
    lines = f.readlines()

# Fix the duplicate filter issue
fixed_lines = []
skip_next_continue = False
prev_line_was_metadata_check = False

for i, line in enumerate(lines):
    # Check if this is a metadata filter line
    if 'if filename.endswith("_metadata.json"):' in line:
        if prev_line_was_metadata_check:
            # Skip duplicate filter
            continue
        prev_line_was_metadata_check = True
        fixed_lines.append(line)
    elif 'continue' in line and prev_line_was_metadata_check:
        # Add continue only once after metadata check
        fixed_lines.append(line)
        prev_line_was_metadata_check = False
        skip_next_continue = True
    elif 'continue' in line and skip_next_continue:
        # Skip duplicate continue
        skip_next_continue = False
        continue
    else:
        prev_line_was_metadata_check = False
        fixed_lines.append(line)

# Write back
with open('backend/app/main.py', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Removed duplicate metadata filters")
