from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os

router = APIRouter()
CONVERTED_DIR = "converted"
EXTENSION = ".gpkg"

os.makedirs(CONVERTED_DIR, exist_ok=True)

@router.get("/download/{filename}")
async def download_converted_file(filename: str):
    """
    📦 Télécharger un fichier .gpkg converti depuis /converted/
    """
    path = os.path.join(CONVERTED_DIR, filename)
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "❌ Fichier .gpkg non trouvé."})
    return FileResponse(path, filename=filename)

@router.delete("/cleanup")
async def cleanup_converted():
    """
    🧹 Supprime tous les fichiers .gpkg du dossier /converted/
    """
    deleted_files = []
    for f in os.listdir(CONVERTED_DIR):
        if f.lower().endswith(EXTENSION):
            os.remove(os.path.join(CONVERTED_DIR, f))
            deleted_files.append(f)

    return {
        "message": "✅ Nettoyage terminé.",
        "deleted": deleted_files or "Aucun fichier à supprimer."
    }

@router.get("/list")
async def list_converted_files():
    """
    📋 Liste tous les fichiers .gpkg disponibles dans /converted/
    """
    files = [f for f in os.listdir(CONVERTED_DIR) if f.lower().endswith(EXTENSION)]
    return {
        "nb_fichiers": len(files),
        "fichiers": files
    }
