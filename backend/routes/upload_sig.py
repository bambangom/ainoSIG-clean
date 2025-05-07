from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.analyse_sig import analyser_sig
from utils.export import generer_rapport
from utils.ia_explainer import expliquer_erreurs
import os
import shutil
import zipfile
import traceback
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
RESULT_DIR = "results"
TEMP_DIR = "temp_extract"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/upload")
async def upload_sig_file(file: UploadFile = File(...)):
    """
    📥 Route pour téléverser un fichier SIG (.shp, .geojson, .gpkg ou .zip),
    l’analyser, générer un résumé IA, et produire les rapports PDF/Excel.
    """
    try:
        ext = os.path.splitext(file.filename)[-1].lower()
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 🔁 Si ZIP : extraction
        if ext == ".zip":
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(TEMP_DIR)

            shp_files = [
                f for f in os.listdir(TEMP_DIR)
                if f.lower().endswith((".shp", ".geojson", ".gpkg"))
            ]
            if not shp_files:
                raise HTTPException(status_code=400, detail="❌ Aucun fichier SIG valide trouvé dans le .zip.")

            file_path = os.path.join(TEMP_DIR, shp_files[0])

        elif ext not in [".shp", ".geojson", ".gpkg"]:
            raise HTTPException(status_code=400, detail="❌ Extension non supportée. Utilisez .shp, .geojson ou .gpkg")

        # 🧪 Analyse SIG
        erreurs, stats = analyser_sig(file_path)

        # 🧠 Résumé IA
        try:
            resume = expliquer_erreurs(stats)
        except Exception as e:
            resume = f"⚠️ Erreur lors de l’appel à l’IA : {str(e)}"

        # 📄 Génération rapports avec horodatage
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path, excel_path = generer_rapport(erreurs, resume, RESULT_DIR, horodatage=horodatage, stats=stats)

        # ✅ Réponse finale
        return {
            "message": "✅ Fichier SIG analysé avec succès.",
            "filename": file.filename,
            "nb_erreurs": stats,
            "resume_ia": resume,
            "downloads": {
                "pdf": f"/results/{os.path.basename(pdf_path)}",
                "excel": f"/results/{os.path.basename(excel_path)}"
            }
        }

    except Exception as e:
        print("❌ ERREUR INTERNE :", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erreur interne : {str(e)}")

    finally:
        # 🧹 Nettoyage des fichiers extraits
        for f in os.listdir(TEMP_DIR):
            try:
                os.remove(os.path.join(TEMP_DIR, f))
            except:
                pass
