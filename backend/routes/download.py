from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import zipfile

router = APIRouter()
RESULT_DIR = "results"

@router.get("/results/download/{timestamp}")
async def download_reports(timestamp: str):
    """
    📦 Télécharge un zip contenant les rapports PDF + Excel pour une session donnée.
    """
    pdf_name = f"resume_ia_{timestamp}.pdf"
    xlsx_name = f"audit_erreurs_{timestamp}.xlsx"
    zip_name = f"rapport_SIG_{timestamp}.zip"

    pdf_path = os.path.join(RESULT_DIR, pdf_name)
    xlsx_path = os.path.join(RESULT_DIR, xlsx_name)
    zip_path = os.path.join(RESULT_DIR, zip_name)

    if not os.path.exists(pdf_path) or not os.path.exists(xlsx_path):
        raise HTTPException(status_code=404, detail="Rapports PDF ou Excel introuvables.")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(pdf_path, arcname=pdf_name)
        zipf.write(xlsx_path, arcname=xlsx_name)

    return FileResponse(zip_path, media_type="application/zip", filename=zip_name)
