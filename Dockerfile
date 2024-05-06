# Utilisez une image de base Python officielle
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de requirements et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000


# Définir la variable d'environnement FLASK_APP ("__init__.py" par défaut)
ENV FLASK_APP=app:create_app

# Définir la variable d'environnement FLASK_ENV (production par défaut)
ENV FLASK_ENV=development

# Définir la variable d'environnement OAUTHLIB_INSECURE_TRANSPORT à 1 pour désactiver la vérification SSL
ENV OAUTHLIB_INSECURE_TRANSPORT=1

# Commande pour exécuter l'application
CMD ["flask", "run", "--host=0.0.0.0"]
