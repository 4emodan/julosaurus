import os
import shutil
import uuid
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

UPLOAD_DIR = "uploads"
IMAGES_DIR = "images"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

class Photo(BaseModel):
    id: str
    url: str

@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/style.css")
async def read_css():
    return FileResponse("style.css")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

@app.post("/upload", response_model=Photo)
async def upload_photo(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension: {file_extension}")

    photo_id = str(uuid.uuid4())
    filename = f"{photo_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return Photo(id=photo_id, url=f"/uploads/{filename}")

@app.get("/photos", response_model=List[Photo])
async def list_photos():
    photos = []
    # If uploads is empty, maybe we want to show images/ as default?
    # Actually, index.html handles the case where it gets an empty list by showing defaults if it's in static mode,
    # but here we have a backend.
    for filename in os.listdir(UPLOAD_DIR):
        if os.path.isfile(os.path.join(UPLOAD_DIR, filename)):
            photo_id = os.path.splitext(filename)[0]
            photos.append(Photo(id=photo_id, url=f"/uploads/{filename}"))
    return photos

# Serve uploads and images
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
