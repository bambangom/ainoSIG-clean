from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes backend
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

# 🔧 Dossier public compilé
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

# 📦 Servir le frontend
app.mount("/assets", StaticFiles(directory=os.path.join(PUBLIC_DIR, "assets")), name="assets")
app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(PUBLIC_DIR, "index.html"))
