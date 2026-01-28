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
STATIC_DIR = "static"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

class Photo(BaseModel):
    id: str
    url: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

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
    for filename in os.listdir(UPLOAD_DIR):
        if os.path.isfile(os.path.join(UPLOAD_DIR, filename)):
            # We use filename as ID for simplicity or uuid if we want to be more strict
            photo_id = os.path.splitext(filename)[0]
            photos.append(Photo(id=photo_id, url=f"/uploads/{filename}"))
    return photos

# Serve uploads and static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
