from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/download/{filename}")
async def download_converted_gpkg(filename: str):
    path = os.path.join("converted", filename)
    if not os.path.exists(path):
        return {"error": "Fichier .gpkg non trouvé"}
    return FileResponse(path, filename=filename)
