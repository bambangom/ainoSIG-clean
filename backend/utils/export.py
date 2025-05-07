import os
import json
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def geojson_to_df(geojson_data):
    """
    Transforme un GeoJSON (str ou dict) en DataFrame pandas.
    Seule la partie 'properties' + type géométrique est conservée.
    """
    if isinstance(geojson_data, str):
        geojson_data = json.loads(geojson_data)

    rows = []
    for f in geojson_data.get('features', []):
        props = f.get('properties', {})
        props['geometry_type'] = f.get('geometry', {}).get('type', 'N/A')
        rows.append(props)

    return pd.DataFrame(rows)

def generer_rapport(erreurs_dict, resume_ia, dossier_resultats, stats=None, horodatage=None):
    """
    Génère les fichiers de sortie :
    - Excel avec les entités en erreur (multi-feuilles + synthèse)
    - PDF avec le résumé IA bien formaté
    """
    os.makedirs(dossier_resultats, exist_ok=True)

    # 📅 Horodatage personnalisé ou automatique
    if not horodatage:
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_path = os.path.join(dossier_resultats, f"audit_erreurs_{horodatage}.xlsx")
    pdf_path = os.path.join(dossier_resultats, f"resume_ia_{horodatage}.pdf")

    # 1. 📊 Génération Excel
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

    # 🧾 Feuille synthèse des statistiques
    if stats:
        df_stats = pd.DataFrame([stats])
        df_stats.to_excel(writer, sheet_name="Synthese", index=False)

    # 📂 Feuilles d'erreurs par type
    for nom, geojson in erreurs_dict.items():
        df = geojson_to_df(geojson)
        feuille = nom[:31] or "Erreur"
        df.to_excel(writer, sheet_name=feuille, index=False)

    writer.close()

    # 2. 🧠 Génération PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "🧠 Rapport IA – Audit SIG – GEO-AINO SUPREME™")
    c.setFont("Helvetica", 10)

    y = height - 80
    for line in resume_ia.splitlines():
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50
        c.drawString(50, y, line.strip())
        y -= 15

    c.save()

    return pdf_path, excel_path
