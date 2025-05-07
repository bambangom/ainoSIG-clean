from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# 📦 Import des routes personnalisées
from routes import (
    upload_sig,
    upload_dxf,
    upload_dgn,
    download,
    cleanup_results,
    download_all,
    download_gpkg  # ✅ renommé pour plus de clarté
)

# 🛠️ Initialisation de l'application FastAPI
app = FastAPI(
    title="GEO-AINO SUPREME™ API",
    description="Plateforme d’audit intelligent des fichiers géospatiaux (SIG, DXF, DGN) propulsée par GPT",
    version="1.0.0"
)

# 🔐 Middleware CORS – à restreindre en production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ en prod : limiter aux domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Création des répertoires requis
os.makedirs("uploaded_files", exist_ok=True)
os.makedirs("results", exist_ok=True)
os.makedirs("results/archives", exist_ok=True)
os.makedirs("converted", exist_ok=True)  # GPKG convertis

# 🌐 Assets frontend (React/Vite ou autre)
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

# 🏠 Route SPA (page HTML principale)
@app.get("/", include_in_schema=False)
async def serve_frontend():
    return FileResponse("../frontend/dist/index.html")

# 🎯 Page d'accueil visible sur Swagger
@app.get("/welcome", tags=["Accueil"])
async def root():
    return {"message": "Bienvenue sur l’API GEO-AINO SUPREME™ 🎯"}

# 🔁 Inclusion des routes métiers
app.include_router(upload_sig.router, prefix="/sig", tags=["Fichiers SIG"])
app.include_router(upload_dxf.router, prefix="/dxf", tags=["Fichiers DXF"])
app.include_router(upload_dgn.router, prefix="/dgn", tags=["Fichiers DGN"])
app.include_router(download.router, prefix="/results", tags=["Téléchargements"])
app.include_router(download_all.router, prefix="/results", tags=["Téléchargement groupé"])
app.include_router(cleanup_results.router, prefix="/results", tags=["Nettoyage"])
app.include_router(download_gpkg.router, prefix="/converted", tags=["Fichiers Convertis"])  # ✅ renommé et intégré
