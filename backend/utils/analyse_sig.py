import geopandas as gpd
from shapely.validation import explain_validity
import json
import os
import zipfile
import tempfile

def extraire_fichier_shp_depuis_zip(zip_path):
    """
    Extrait un fichier .shp depuis une archive .zip et retourne le chemin du fichier principal .shp extrait.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        temp_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_dir)
        for file in os.listdir(temp_dir):
            if file.lower().endswith(".shp"):
                return os.path.join(temp_dir, file)
        raise ValueError("Archive ZIP invalide : aucun fichier .shp trouvé.")

def analyser_sig(file_path):
    """
    Analyse un fichier SIG (.shp, .geojson, .gpkg ou .zip) :
    - Retourne les entités fautives (GeoJSON)
    - Fournit un résumé statistique
    """

    # ⚙️ Gérer les fichiers .zip contenant un .shp
    if file_path.lower().endswith(".zip"):
        try:
            file_path = extraire_fichier_shp_depuis_zip(file_path)
        except Exception as e:
            raise RuntimeError(f"Erreur d'extraction ZIP : {e}")

    try:
        gdf = gpd.read_file(file_path)
    except Exception as e:
        raise RuntimeError(f"Erreur de lecture du fichier SIG : {e}")

    # S'assurer que la colonne NICAD existe
    if 'NICAD' not in gdf.columns:
        gdf['NICAD'] = ''

    gdf['NICAD'] = gdf['NICAD'].astype(str).str.strip()
    gdf['ID_NICAD'] = gdf['NICAD'].apply(lambda x: x if len(x) == 16 else '')

    gdf_valid = gdf[gdf['ID_NICAD'] != '']

    erreurs = {
        'doublons_geom': gdf_valid[gdf_valid.duplicated(subset='geometry', keep=False)].to_json(),
        'doublons_nicad': gdf_valid[gdf_valid.duplicated(subset='ID_NICAD', keep=False)].to_json(),
        'invalides': gdf_valid[~gdf_valid.is_valid].assign(
            reason=gdf_valid[~gdf_valid.is_valid].geometry.apply(explain_validity)
        ).to_json(),
        'vides': gdf_valid[gdf_valid.geometry.is_empty].to_json(),
        'surfaces_nulles': gdf_valid[gdf_valid.geometry.area <= 0.01].to_json()
    }

    stats = {
        'doublons_geom': len(json.loads(erreurs['doublons_geom'])['features']),
        'doublons_nicad': len(json.loads(erreurs['doublons_nicad'])['features']),
        'invalides': len(json.loads(erreurs['invalides'])['features']),
        'vides': len(json.loads(erreurs['vides'])['features']),
        'surfaces_nulles': len(json.loads(erreurs['surfaces_nulles'])['features']),
        'total': len(gdf)
    }

    return erreurs, stats
