"""
Controlleur pour les routes des vue liées aux clients
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.models import database
import app.models.ebp as ebp
import app.models.zeendoc as zeendoc


v_client_bp = Blueprint("v_client", __name__)

@v_client_bp.route("/form_add_client", methods=["GET"])
@login_required
def form_add_client():
    """Route pour afficher le formulaire d'ajout d'un client"""
    return render_template("client/add_client.html")


@v_client_bp.route("/fill_requiert/<int:id_client>", methods=["GET"])
@login_required
def form_add_multiple_requiert(id_client):
    """Route pour afficher le formulaire d'ajout de plusieurs clients"""
    filled_fields = database.get_champ_passerelle_client_by_client_with_lib_champ(id_client)
    fields = database.get_champ_by_client_with_lib_champ(id_client)

    # on verifie si EBP_FOLDER_ID est dans les champs requis
    liste_ebp_folder = []
    liste_zeendoc_classeur = []

    for field in fields:
        if field["LibChamp"] == "EBP_FOLDER_ID":
            try:
                instance_ebp = ebp.EBP(id_client)
                liste_ebp_folder = instance_ebp.get_folders()

            except:
                liste_ebp_folder = []


        if field["LibChamp"] == "Zeendoc_CLASSEUR":
            try:
                instance_zeendoc = zeendoc.Zeendoc(id_client)
                liste_zeendoc_classeur = instance_zeendoc.get_classeurs()

            except:
                liste_zeendoc_classeur = []




    return render_template("client/add_multiple_requiert.html", fields=fields, id_client=id_client, liste_ebp_folder=liste_ebp_folder, liste_zeendoc_classeur=liste_zeendoc_classeur)
