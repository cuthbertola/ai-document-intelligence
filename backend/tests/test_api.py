"""Test API endpoints"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_api_health():
    """Test health endpoint with requests"""
    import requests
    try:
        # Try to connect to the API
        response = requests.get("http://localhost:8000/api/ocr/health", timeout=2)
        assert response.status_code == 200
        print("API health check passed")
    except requests.exceptions.RequestException:
        print("API server not running - start it with: uvicorn app.main:app --reload")

def test_app_routes():
    """Test that routes are registered"""
    from app.main import app
    routes = [r.path for r in app.routes]
    ocr_routes = [r for r in routes if '/api/ocr' in r]
    assert len(ocr_routes) > 0
    print(f"Found {len(ocr_routes)} OCR routes")
    for route in ocr_routes:
        print(f"  - {route}")
