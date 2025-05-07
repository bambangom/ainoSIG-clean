from fastapi import APIRouter
from pydantic import BaseModel
import openai
import os
import geopandas as gpd

router = APIRouter()

UPLOAD_DIR = "uploaded_files"

class ChatRequest(BaseModel):
    question: str
    filename: str

@router.post("/ask_ai")
async def ask_ai(req: ChatRequest):
    """
    💬 Permet de poser une question personnalisée sur un fichier analysé.
    L’IA répond en fonction du contenu du fichier et du contexte cadastral DGID.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    file_path = os.path.join(UPLOAD_DIR, req.filename)

    if not os.path.exists(file_path):
        return {"reponse": f"⚠️ Fichier non trouvé : {req.filename}"}

    try:
        gdf = gpd.read_file(file_path)
        stats = {
            "Total": len(gdf),
            "Champs disponibles": list(gdf.columns),
            "Extrait NICAD": list(gdf["NICAD"].dropna().unique()[:5]) if "NICAD" in gdf.columns else "Non disponible",
        }

        # 🔥 PROMPT OPTIMISÉ
        prompt = f"""
Tu es un assistant cadastral intelligent, expert SIG au Sénégal, formé aux normes de la DGID, au processus QGIS et au traitement des fichiers DAO (DXF, DGN) et SIG (SHP, GeoJSON, GPKG).

Un agent DGID t’a soumis une question relative à un fichier géographique contenant {stats["Total"]} entités.

Voici des informations utiles sur le fichier :
- Champs disponibles : {', '.join(stats['Champs disponibles'])}
- Échantillon NICAD : {stats['Extrait NICAD']}

Ta mission :
1. Comprendre précisément la question suivante :  
   👉 « {req.question} »

2. Y répondre de façon claire, concise et immédiatement exploitable par un agent DGID ou un géomètre en :
   - mission terrain
   - traitement bureau (SIG ou DAO)
   - contrôle qualité ou régularisation

3. Adapte ta réponse au contexte cadastral sénégalais :
   - Explique s’il y a lieu de vérifier une topologie, une attribution NICAD, une erreur de calque, une incohérence attributaire
   - Propose des outils (QGIS, GDAL, AutoCAD, terrain) ou commandes utiles si besoin
   - Utilise un langage simple mais professionnel

Ne fais pas de résumé général : concentre-toi uniquement sur la **question posée**, dans **le contexte du fichier analysé**. Tu es là pour assister de façon intelligente et pragmatique.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant cadastral DGID sénégalais expert en SIG."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        return {"reponse": response.choices[0].message["content"]}

    except Exception as e:
        return {"reponse": f"⚠️ Erreur IA : {str(e)}"}
