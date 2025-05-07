from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.analyse_dgn import analyser_dgn
from utils.export import generer_rapport
from utils.ia_explainer import expliquer_erreurs
import os
import shutil
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
RESULT_DIR = "results"
CONVERTED_DIR = "converted"
ALLOWED_EXTENSIONS = [".dgn", ".gpkg"]

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)

@router.post("/upload")
async def upload_dgn_file(file: UploadFile = File(...)):
    """
    📥 Téléverse un fichier .DGN ou .GPKG, le traite, génère les rapports + lien .gpkg.
    """
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="❌ Extension non supportée. Utilisez uniquement un fichier .dgn ou .gpkg"
        )

    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 🧪 Analyse (conversion si DGN, sinon GPKG direct)
        erreurs, stats, gpkg_path = analyser_dgn(file_path)

        # 🧠 Résumé IA
        try:
            resume = expliquer_erreurs(stats)
        except Exception as e:
            resume = f"⚠️ Erreur IA : {str(e)}"

        # 📄 Génération de rapport horodaté
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path, excel_path = generer_rapport(erreurs, resume, RESULT_DIR, stats=stats)

        # ✅ Réponse avec lien de téléchargement GPKG
        return {
            "message": "✅ Fichier analysé avec succès.",
            "filename": filename,
            "nb_erreurs": stats,
            "resume_ia": resume,
            "downloads": {
                "pdf": f"/results/{os.path.basename(pdf_path)}",
                "excel": f"/results/{os.path.basename(excel_path)}",
                "gpkg": f"/converted/{os.path.basename(gpkg_path)}"
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Erreur durant le traitement DGN : {str(e)}")
