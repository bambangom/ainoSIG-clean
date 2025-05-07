import geopandas as gpd
import subprocess
import os
import uuid
from .analyse_sig import analyser_sig

def analyser_dxf(file_path):
    """
    Convertit un fichier DXF en GeoPackage, puis l’analyse comme un fichier SIG.
    Retourne les erreurs et les statistiques.
    """
    # 📌 Préparation du fichier temporaire converti
    output_dir = "converted"
    os.makedirs(output_dir, exist_ok=True)
    basename = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_dir, f"{basename}_{uuid.uuid4().hex[:8]}.gpkg")

    # 🛠️ Conversion DXF ➜ GPKG via ogr2ogr
    try:
        subprocess.run([
            "ogr2ogr",
            "-f", "GPKG",
            output_path,
            file_path
        ], check=True)
    except Exception as e:
        raise RuntimeError(f"Erreur de conversion DXF : {e}")

    # 📊 Analyse comme un SIG classique
    erreurs, stats = analyser_sig(output_path)

    return erreurs, stats
