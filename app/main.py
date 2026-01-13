from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from app.services import ImageService
from typing import Optional

app = FastAPI(title="Instagram Service Layer")

@app.post("/upload")
async def upload(user_id: str, category: str, file: UploadFile = File(...)):
    try:
        # FastAPI's 'file.file' is a SpooledTemporaryFile compatible with upload_fileobj
        result = ImageService.upload_image(file.file, file.filename, user_id, category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/images")
async def list_imgs(filter_key: Optional[str] = None, filter_value: Optional[str] = None):
    return ImageService.list_images(filter_key, filter_value)

@app.get("/images/{image_id}/download")
async def download(image_id: str):
    url = ImageService.get_presigned_url(image_id)
    if not url:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"download_url": url}

@app.delete("/images/{image_id}")
async def delete(image_id: str):
    success = ImageService.delete_image(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}