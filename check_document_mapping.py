#!/usr/bin/env python3
from pathlib import Path

uploads = Path("data/uploads")
processed = Path("data/processed")

print("=== Files in uploads ===")
for f in uploads.glob("*.pdf"):
    print(f"  📁 {f.name}")
    # Check if text file exists in processed
    txt_file = processed / f"{f.stem}.txt"
    if txt_file.exists():
        print(f"    ✅ Has text file: {txt_file.name}")
        with open(txt_file, 'r') as file:
            word_count = len(file.read().split())
        print(f"    📊 Words: {word_count}")
    else:
        print(f"    ❌ No text file found")

print("\n=== Files in processed ===")
txt_files = list(processed.glob("*.txt"))
print(f"Total: {len(txt_files)} text files")
for f in txt_files[:5]:
    with open(f, 'r') as file:
        word_count = len(file.read().split())
    print(f"  📄 {f.name} ({word_count} words)")
