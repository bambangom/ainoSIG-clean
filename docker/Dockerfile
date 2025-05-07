# Dockerfile à placer à la racine du projet (geo-aino-supreme/)

# Étape 1 – Build du frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

# Étape 2 – Backend + assets
FROM python:3.11-slim AS backend

# Dépendances système utiles
RUN apt-get update && apt-get install -y \
    gdal-bin python3-gdal python3-dev build-essential libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
WORKDIR /app
COPY backend/ ./backend/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ajout du frontend déjà buildé
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ports + lancement
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
