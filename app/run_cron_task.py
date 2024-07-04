import sys
import os

# Ajouter le chemin du répertoire de l'application au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import passerelles
import logging

# Configuration du logging
logging.basicConfig(filename='/app/logs/cron_task.log', level=logging.DEBUG)

def run_cron_task():
    logging.debug('Cron task started.')
    passerelles.routine()
    logging.debug('Cron task finished.')

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        run_cron_task()
