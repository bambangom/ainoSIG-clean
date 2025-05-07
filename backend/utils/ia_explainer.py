from openai import OpenAI
from dotenv import load_dotenv
import os

# 🔐 Charger les variables d’environnement depuis le fichier .env
load_dotenv()

# ⚙️ Initialisation du client OpenAI (v1.x)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def expliquer_erreurs(stats: dict) -> str:
    """
    Génère un résumé intelligent des erreurs SIG avec GPT-4
    en tenant compte des normes DGID, DAO, terrain et SIG.
    """
    prompt = f"""
Tu es un expert SIG au Sénégal, spécialisé dans les audits cadastraux, la correction des anomalies géographiques et l’assistance aux agents de la DGID.

Voici les résultats d’un audit automatisé réalisé par le système GEO-AINO SUPREME™ :

- Doublons géométriques : {stats['doublons_geom']}
- Doublons NICAD : {stats['doublons_nicad']}
- Géométries invalides (self-intersections, anneaux mal formés, etc.) : {stats['invalides']}
- Géométries vides : {stats['vides']}
- Surfaces nulles ou aberrantes : {stats['surfaces_nulles']}
- Total des entités analysées : {stats['total']}

Ta mission est la suivante :

1. Expliquer clairement chaque type d’erreur détectée :
   - Quels sont les impacts concrets sur le cadastre ?
   - Quelles erreurs sont critiques et bloquantes pour l’intégration SIG ou fiscale ?
   - Comment se manifestent-elles dans un contexte DAO (DXF/DGN) ou SIG (SHP/GeoJSON) ?

2. Proposer des actions concrètes à l’agent :
   - Quelles corrections manuelles sont possibles dans QGIS ou MicroStation ?
   - Quelles corrections peuvent être automatisées dans GEO-AINO SUPREME™ ?
   - Que faire sur le terrain si les données source sont incorrectes ?

3. Donner des conseils clairs et utiles à un agent DGID :
   - Bonnes pratiques lors de la production de fichiers DAO ou SIG
   - Structuration correcte des champs NICAD, ID, sections
   - Recommandations de contrôle en amont, lors des livraisons DAO
   - Importance de la polygonation, des calques, du nettoyage topologique

4. Adopte un ton professionnel, pédagogique et sénégalais :
   - Tu es un formateur DGID expérimenté, parlant à un collègue
   - Ta réponse doit être compréhensible mais précise, utile en situation réelle
   - Tu peux proposer un ordre de traitement des anomalies, par gravité ou par impact fiscal

Structure bien ta réponse, sans jargon inutile. Ta mission est de renforcer la compétence de l’agent tout en facilitant l’intégration du fichier dans le système cadastral sénégalais.
    """

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en cadastre sénégalais et en audit SIG."
                },
                {
                    "role": "user",
                    "content": prompt.strip()
                }
            ],
            temperature=0.4
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Erreur lors de l’appel à l’IA : {str(e)}"
