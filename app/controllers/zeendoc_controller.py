"""
Ce fichier contient les routes pour les requêtes liées à Zeendoc.
"""

from flask import Blueprint, jsonify
from flask_login import login_required
from app.models.zeendoc import Zeendoc  # pylint: disable=E0401

# Création d'un Blueprint pour le zeendoc controller
zeendoc_bp = Blueprint("zeendoc", __name__)

@zeendoc_bp.route("/get_classeurs_zeendoc/<int:client_id>", methods=["GET"])
@login_required
def get_classeurs_zeendoc(client_id):
    """
    Route pour récupérer les classeurs d'un client dans Zeendoc.
    """
    client = Zeendoc(client_id)
    classeurs = client.get_rights()["Collections"]

    return jsonify(classeurs)
