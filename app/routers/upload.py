from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import cloudinary.uploader
from app.dependencies import verify_admin

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    _: str = Depends(verify_admin)
):
    """Admin: Upload an image to Cloudinary"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            folder="johnson-portfolio",
            resource_type="image"
        )
        
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))