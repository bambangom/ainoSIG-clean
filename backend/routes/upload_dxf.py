from fastapi import APIRouter, UploadFile, File
from utils.analyse_dxf import analyser_dxf
from utils.export import generer_rapport
from utils.ia_explainer import expliquer_erreurs
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@router.post("/upload")
async def upload_dxf_file(file: UploadFile = File(...)):
    """
    📥 Route pour téléverser un fichier .DXF (DAO),
    le convertir en SIG, analyser les entités, et produire un rapport IA.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 🧪 Analyse du fichier DXF via GDAL + GeoPandas
    erreurs, stats = analyser_dxf(file_path)

    # 🧠 Résumé IA (GPT)
    resume = expliquer_erreurs(stats)

    # 📤 Génération rapport (PDF + Excel)
    pdf_path, excel_path = generer_rapport(erreurs, resume, RESULT_DIR)

    return {
        "message": "Fichier DXF analysé avec succès.",
        "filename": file.filename,
        "nb_erreurs": stats,
        "resume_ia": resume,
        "downloads": {
            "pdf": f"/results/{os.path.basename(pdf_path)}",
            "excel": f"/results/{os.path.basename(excel_path)}"
        }
    }
