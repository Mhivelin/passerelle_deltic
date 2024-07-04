#!/bin/bash
# Démarrer cron
service cron start

# Démarrer flask
flask run --host=0.0.0.0
