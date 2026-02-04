# Utiliser une image Python officielle légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer poetry
RUN pip install poetry

# Copier les fichiers de configuration poetry
COPY pyproject.toml poetry.lock ./

# Configurer poetry pour ne pas créer d'environnement virtuel (on est dans Docker)
RUN poetry config virtualenvs.create false

# Installer les dépendances
RUN poetry install --no-interaction --no-ansi

# Copier le code de l'application
COPY . .

# Exposer les ports API (8000) et UI (8080)
EXPOSE 8000 8080

# Commande de démarrage par défaut (lance les deux services)
# Note: Dans un environnement de prod strict, on séparerait les conteneurs.
# Ici pour simplifier l'exercice TP, on lance tout ensemble.
CMD ["sh", "-c", "uvicorn webserv:app --host 0.0.0.0 --port 8000 & python client_ui.py"]
