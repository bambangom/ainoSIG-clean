from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
import zipfile
from datetime import datetime

router = APIRouter()
RESULT_DIR = "results"
TEMP_ZIP = os.path.join(RESULT_DIR, "archives")
os.makedirs(TEMP_ZIP, exist_ok=True)

@router.get("/results/download/all")
async def download_all_results():
    """
    📦 Crée une archive ZIP avec tous les fichiers du dossier /results
    et renvoie un lien de téléchargement.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"rapports_audit_{timestamp}.zip"
        zip_path = os.path.join(TEMP_ZIP, zip_name)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for filename in os.listdir(RESULT_DIR):
                path = os.path.join(RESULT_DIR, filename)
                if os.path.isfile(path) and not filename.endswith(".zip"):
                    zipf.write(path, arcname=filename)

        return FileResponse(zip_path, filename=zip_name, media_type='application/zip')

    except Exception as e:
        return JSONResponse(content={"error": f"Erreur lors de la création du ZIP : {str(e)}"}, status_code=500)
