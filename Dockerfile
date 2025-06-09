FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt package.json package-lock.json* ./

# Installer Node.js, npm et les dépendances nécessaires pour psycopg2
RUN apt-get update && \
    apt-get install -y nodejs npm gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python et JS
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Copier le reste du code
COPY . .

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Commande pour démarrer l'application avec Gunicorn et SSL
CMD ["gunicorn", "--workers=4", "--threads=2", "--timeout=60", "--bind=0.0.0.0:5000", "--log-level=info", "--certfile=server.crt", "--keyfile=server.key", "app:app"]
