from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os

router = APIRouter()
RESULT_DIR = "results"
EXTENSIONS_TO_DELETE = [".xlsx", ".pdf", ".zip"]

@router.delete("/results/cleanup")
async def cleanup_results():
    """
    🧹 Supprime tous les fichiers générés dans le dossier results/
    (PDF, Excel, ZIP).
    """
    deleted_files = []
    if not os.path.exists(RESULT_DIR):
        return JSONResponse(content={"message": "📁 Aucun dossier 'results' trouvé."}, status_code=200)

    for f in os.listdir(RESULT_DIR):
        file_path = os.path.join(RESULT_DIR, f)
        if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in EXTENSIONS_TO_DELETE:
            os.remove(file_path)
            deleted_files.append(f)

    return {
        "message": "✅ Nettoyage effectué.",
        "deleted_files": deleted_files or "Aucun fichier à supprimer."
    }
