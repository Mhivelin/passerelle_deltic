"""
Ce script exécute une tâche cron pour l'application Flask.
"""

import logging
import os
import sys

from app import create_app
from app.models import passerelles

# Ajouter le chemin du répertoire de l'application au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


def run_cron_task():
    """
    Exécute la tâche cron définie dans le module passerelles.
    """

    logger.info("Cron task started.")
    passerelles.routine()
    logger.info("Cron task finished.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_cron_task()
