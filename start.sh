#!/bin/bash

# Démarrer le service cron
service cron start

# Attendre un moment pour s'assurer que cron a démarré
sleep 5

# Démarrer Flask
flask run --host=0.0.0.0
