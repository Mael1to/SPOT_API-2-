# Utilisation d'une image Python
FROM python:3.9

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Lancer Django
CMD ["python", "spotynov_api/manage.py", "runserver", "0.0.0.0:8000"]
