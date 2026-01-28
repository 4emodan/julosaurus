import os
import shutil
import pytest
from fastapi.testclient import TestClient
from main import app, UPLOAD_DIR
import io

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: ensure UPLOAD_DIR exists and is empty
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)
    yield
    # Teardown: clean up UPLOAD_DIR
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
    os.makedirs(UPLOAD_DIR)

def test_upload_photo():
    file_content = b"fake image content"
    file = io.BytesIO(file_content)

    response = client.post(
        "/upload",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "url" in data
    assert data["url"].startswith("/uploads/")

    filename = data["url"].split("/")[-1]
    assert os.path.exists(os.path.join(UPLOAD_DIR, filename))

def test_upload_unsupported_extension():
    file = io.BytesIO(b"some content")
    response = client.post(
        "/upload",
        files={"file": ("test.txt", file, "image/jpeg")}
    )
    assert response.status_code == 400
    assert "Unsupported file extension" in response.json()["detail"]

def test_upload_not_an_image_mime():
    file = io.BytesIO(b"some content")
    response = client.post(
        "/upload",
        files={"file": ("test.jpg", file, "text/plain")}
    )
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"]

def test_list_photos():
    # Upload one photo first
    client.post(
        "/upload",
        files={"file": ("test.png", io.BytesIO(b"img"), "image/png")}
    )

    response = client.get("/photos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
