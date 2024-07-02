"""
Ce module contient les routes pour les différentes entités du modèle Passerelle.
"""

from flask import Blueprint
from flask_login import login_required
import logging
from app.models import passerelles

# Création d'un Blueprint pour le controller
passerelle_bp = Blueprint('passerelle_controller', __name__)

@passerelle_bp.route('/routine', methods=['GET'])
@login_required
def routine():
    """
    Route pour lancer la routine de remontée de paiement.
    """
    logging.info("Routine de remontée de paiement lancée.")
    return passerelles.routine()