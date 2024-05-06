"""
Controlleur pour les routes des vue liées aux logiciels
"""

from flask import Blueprint,  render_template, request
from flask_login import login_required
from app.models import database

# Création d'un Blueprint pour le logiciel controller
v_logiciel_bp = Blueprint("logiciel", __name__)

@v_logiciel_bp.route("/form_add_logiciel", methods=["GET"])
@login_required
def form_add_logiciel():
    """Route pour afficher le formulaire d'ajout d'un logiciel"""
    return render_template("logiciel/add_logiciel.html")



