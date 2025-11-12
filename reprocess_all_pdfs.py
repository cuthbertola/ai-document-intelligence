#!/usr/bin/env python3
import requests
import time
import os

print("🔄 Batch Processing All Documents")
print("=" * 50)

# Check if backend is running
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✅ Backend is running")
except:
    print("❌ Backend is not running!")
    exit(1)

# Get all documents
response = requests.get("http://localhost:8000/api/v1/documents?limit=100")
documents = response.json()["documents"]

print(f"📁 Found {len(documents)} documents to process\n")

success = 0
failed = 0
already_processed = 0

for doc in documents:
    doc_id = doc["id"]
    filename = doc["filename"]
    status = doc.get("status", "unknown")
    
    print(f"[{doc_id}] {filename}")
    
    if status == "completed":
        print("  ✓ Already processed")
        already_processed += 1
        continue
    
    try:
        response = requests.post(f"http://localhost:8000/api/v1/process/{doc_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success! Words: {data.get('word_count', 0)}")
            success += 1
        else:
            print(f"  ❌ Failed: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"  ❌ Error: {e}")
        failed += 1
    
    time.sleep(0.5)  # Small delay between requests

print("\n" + "=" * 50)
print(f"✅ Successfully processed: {success}")
print(f"⏭️  Already processed: {already_processed}")
print(f"❌ Failed: {failed}")
print("\n�� Checking processed folder...")

# Check results
processed_dir = "/Users/olawalebadekale/ai-document-platform/data/processed"
txt_files = [f for f in os.listdir(processed_dir) if f.endswith('.txt')]
json_files = [f for f in os.listdir(processed_dir) if f.endswith('_metadata.json')]

print(f"📄 Text files: {len(txt_files)}")
print(f"📋 Metadata files: {len(json_files)}")

if txt_files:
    print("\nSample text files created:")
    for f in txt_files[:5]:
        file_path = os.path.join(processed_dir, f)
        size = os.path.getsize(file_path)
        print(f"  - {f} ({size:,} bytes)")

print("\n✅ Done! Check your frontend to see the extracted text!")
