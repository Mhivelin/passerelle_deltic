"""
Controlleur pour les routes des vue liées aux passerelles
"""

from flask import Blueprint,  render_template, request
from flask_login import login_required
from app.models import database

# Création d'un Blueprint pour le passerelle controller
v_passerelle_bp = Blueprint("passerelle", __name__)



@v_passerelle_bp.route("/form_add_passerelle", methods=["GET"])
@login_required
def form_add_passerelle():
    """Route pour afficher le formulaire d'ajout d'une passerelle"""
    logiciels = database.get_all_logiciels()
    champs = database.get_all_champs()
    print(champs)
    return render_template("passerelle/add_passerelle.html", logiciels=logiciels, champs=champs)


@v_passerelle_bp.route("/form_connect_passerelle", methods=["GET"])
@login_required
def form_connect_passerelle():
    """Route pour afficher le formulaire de connexion d'une passerelle"""
    # on recupère l'id du client
    id_client = request.args.get("IdClient")
    passerelles = database.get_all_passerelles()

    client =  database.get_client_by_id(id_client)
    return render_template("connect_passerelle.html",
                           passerelles=passerelles,
                           id_client=id_client,
                           client=client)
