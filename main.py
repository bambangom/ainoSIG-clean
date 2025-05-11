from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.routes import (
    upload_sig,
    upload_dgn,
    upload_dxf,
    download,
    download_all,
    download_gpkg,
    converted,
    cleanup_results,
    ask_ai,
)

app.include_router(upload_sig.router)
app.include_router(upload_dgn.router)
app.include_router(upload_dxf.router)
app.include_router(download.router)
app.include_router(download_all.router)
app.include_router(download_gpkg.router)
app.include_router(converted.router)
app.include_router(cleanup_results.router)
app.include_router(ask_ai.router)

# ✅ Mettre à jour ici pour Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "public")
ASSETS_DIR = os.path.join(FRONTEND_DIST, "assets")

if not os.path.exists(FRONTEND_DIST):
    raise RuntimeError(f"⚠️ Le dossier {FRONTEND_DIST} est introuvable. Lance `npm run build` puis copie-le dans `public/`.")

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/static", StaticFiles(directory=FRONTEND_DIST), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
