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

# Copier le fichier crontab et donner les droits d'exécution
COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Appliquer la crontab et lancer le service cron
RUN crontab /etc/cron.d/my-cron-job

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000

# Définir la variable d'environnement FLASK_APP ("__init__.py" par défaut)
ENV FLASK_APP=app:create_app

# Définir la variable d'environnement FLASK_ENV (production par défaut)
ENV FLASK_ENV=development

# Définir la variable d'environnement OAUTHLIB_INSECURE_TRANSPORT à 1 pour désactiver la vérification SSL
ENV OAUTHLIB_INSECURE_TRANSPORT=1

# Commande pour exécuter l'application
CMD ["sh", "-c", "service cron start && flask run --host=0.0.0.0"]
