import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_health_check():
    """Verify the API is awake."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_upload_and_list_flow():
    """Test the full lifecycle: Upload -> List -> Metadata Check."""
    
    # 1. Create a fake image
    file_name = "test_image.jpg"
    file_content = b"fake_binary_data_for_testing"
    file = io.BytesIO(file_content)
    
    # 2. POST to /upload
    params = {"user_id": "reviewer_1", "category": "automation"}
    files = {"file": (file_name, file, "image/jpeg")}
    
    upload_response = client.post("/upload", params=params, files=files)
    assert upload_response.status_code == 200
    
    data = upload_response.json()
    assert data["filename"] == file_name
    assert "image_id" in data
    
    # 3. List images and verify our upload is there
    list_response = client.get("/images", params={"filter_key": "user_id", "filter_value": "reviewer_1"})
    assert list_response.status_code == 200
    items = list_response.json()
    assert any(item["image_id"] == data["image_id"] for item in items)

def test_get_download_url():
    """Verify we can generate a presigned URL for an uploaded image."""
    # Note: This assumes an image exists or uses the one from previous test if using a shared DB
    response = client.get("/images")
    items = response.json()
    if items:
        img_id = items[0]["image_id"]
        res = client.get(f"/images/{img_id}/download")
        assert res.status_code == 200
        assert "download_url" in res.json()
        assert ":4566" in res.json()["download_url"]