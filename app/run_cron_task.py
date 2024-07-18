import os
import sys
import fcntl
import logging

# Ajouter le chemin du répertoire de l'application au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import passerelles

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/app/logs/cron_task.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

LOCK_FILE = "/tmp/my_cron_task.lock"

def run_cron_task():
    """
    Exécute la tâche cron définie dans le module passerelles.
    """
    logger.info("Starting cron task")
    passerelles.routine()
    logger.info("Cron task completed")

if __name__ == "__main__":
    # Création de l'application Flask
    app = create_app()
    with app.app_context():
        # Mise en place du verrouillage pour éviter les superpositions
        with open(LOCK_FILE, 'w') as lock_file:
            try:
                fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                run_cron_task()
            except IOError:
                logger.info("Cron task already running")
