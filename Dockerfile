# Utilisez une image de base Python officielle
FROM python:3.8

# Installer cron
RUN apt-get update && apt-get install -y cron

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY . .

# Créer un répertoire pour les logs et donner les droits d'accès
RUN mkdir -p /app/logs && chmod 0777 /app/logs

# Assurer que le répertoire de la base de données a les bonnes permissions
RUN mkdir -p /app/instance && chmod -R 0777 /app/instance

# Copier le fichier crontab et donner les droits d'exécution
COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Appliquer la crontab
RUN crontab /etc/cron.d/my-cron-job

# Copier et donner les droits d'exécution au script de démarrage
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000

# Définir les variables d'environnement
ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development
ENV OAUTHLIB_INSECURE_TRANSPORT=1
ENV PYTHONPATH=/app

# Utiliser le script de démarrage
CMD ["/start.sh"]
