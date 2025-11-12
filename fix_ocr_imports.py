#!/usr/bin/env python3
import os

ocr_file = "/Users/olawalebadekale/ai-document-platform/backend/app/services/ocr_service.py"

# Read the file
with open(ocr_file, 'r') as f:
    content = f.read()

# Make cv2 import optional
old_import = "import cv2"
new_import = """try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: cv2 not available, image preprocessing disabled")"""

if old_import in content and "CV2_AVAILABLE" not in content:
    content = content.replace(old_import, new_import)
    
    # Also update the preprocess_image method to check CV2_AVAILABLE
    content = content.replace(
        "def preprocess_image(self, image: np.ndarray) -> np.ndarray:",
        "def preprocess_image(self, image: np.ndarray) -> np.ndarray:\n        if not CV2_AVAILABLE:\n            return image"
    )
    
    # Save the file
    with open(ocr_file, 'w') as f:
        f.write(content)
    
    print("✅ Fixed OCR service to make cv2 optional")
else:
    print("OCR service already fixed or doesn't need fixing")
