import os
import uuid
import subprocess
from .analyse_sig import analyser_sig

def analyser_dgn(file_path):
    """
    Analyse un fichier DGN ou GPKG :
    ✅ Si GPKG : audit direct
    ✅ Si DGN : conversion → GPKG → audit

    🔁 Retourne : erreurs, stats, chemin du fichier .gpkg analysé
    """
    ext = os.path.splitext(file_path)[-1].lower()

    # 📁 Répertoire pour fichiers convertis
    output_dir = "converted"
    os.makedirs(output_dir, exist_ok=True)

    if ext == ".gpkg":
        # ✅ Analyse directe du GPKG
        erreurs, stats = analyser_sig(file_path)
        return erreurs, stats, file_path

    elif ext == ".dgn":
        # 🛠️ Préparation conversion
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        unique_id = uuid.uuid4().hex[:8]
        gpkg_path = os.path.join(output_dir, f"{base_name}_{unique_id}.gpkg")

        # 🔧 Définir les variables d’environnement (QGIS/Windows)
        os.environ["GDAL_DATA"] = os.environ.get("GDAL_DATA", r"C:\Program Files\QGIS 3.34.7\share\gdal")
        os.environ["PATH"] += os.pathsep + r"C:\Program Files\QGIS 3.34.7\bin"

        # ⚙️ Conversion DGN → GPKG
        try:
            subprocess.run(
                ["ogr2ogr", "-f", "GPKG", gpkg_path, file_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"❌ Erreur de conversion DGN → GPKG :\n{e.stderr.strip()}")

        # ✅ Audit du fichier converti
        erreurs, stats = analyser_sig(gpkg_path)
        return erreurs, stats, gpkg_path

    else:
        raise RuntimeError("❌ Format non reconnu. Utilisez un fichier .dgn ou .gpkg uniquement.")
