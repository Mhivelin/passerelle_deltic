"""
Controlleur pour les routes des vue liées aux clients
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
import logging
from app.models import database
import app.models.ebp as ebp
import app.models.zeendoc as zeendoc


v_client_bp = Blueprint("v_client", __name__)

@v_client_bp.route("/form_add_client", methods=["GET"])
@login_required
def form_add_client():
    """Route pour afficher le formulaire d'ajout d'un client"""
    return render_template("client/add_client.html")









@v_client_bp.route("/fill_requiert/<int:id_passerelle_client>/<int:id_client>", methods=["GET"])
@login_required
def form_add_requiert_passerelle(id_passerelle_client, id_client):
    """Route pour afficher le formulaire d'ajout de plusieurs clients"""
    try:
        # Récupère les champs passerelle client par ID de passerelle client
        filled_fields = database.get_champ_passerelle_client_by_ids_with_lib_champ(id_passerelle_client)

        # Récupère l'ID de passerelle en utilisant l'ID de passerelle client
        id_passerelle = database.get_id_passerelle_by_id_passerelle_client(id_passerelle_client)

        if not id_passerelle:
            return jsonify({"error": "IdPasserelle introuvable pour l'IdPasserelleClient donné"}), 400

        # Récupère les champs par ID de passerelle et les logiciels associés
        fields = database.get_champ_by_passerelle_and_logiciel_passerelle(id_passerelle)

        # Ajoute les valeurs des champs remplis aux champs
        for field in fields:
            for filled_field in filled_fields:
                if field["IdChamp"] == filled_field["IdChamp"]:
                    field["Valeur"] = filled_field["Valeur"]

        liste_ebp_folder, liste_zeendoc_classeur, liste_zeendoc_index = [], [], []

        # Gestion des différents types de champs
        try:
            liste_ebp_folder = fetch_ebp_folders(id_client, fields)
            liste_zeendoc_classeur = fetch_zeendoc_classeurs(id_client, fields)
            liste_zeendoc_index = fetch_zeendoc_indexes(id_client, fields)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des listes: {e}")


        id_passerelle = database.get_id_passerelle_by_id_passerelle_client(id_passerelle_client)

        return render_template(
            "client/add_multiple_requiert.html",
            fields=fields,
            id_client=id_client,
            id_passerelle=id_passerelle,
            liste_ebp_folder=liste_ebp_folder,
            liste_zeendoc_classeur=liste_zeendoc_classeur,
            liste_zeendoc_index=liste_zeendoc_index
        )
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des champs: {e}")
        return jsonify({"error": "Erreur lors de la récupération des champs"}), 500




def fetch_ebp_folders(id_client, fields):
    for field in fields:
        if field.get("TypeChamp") == "select_ebp_folder":
            try:
                instance_ebp = ebp.EBP(id_client)
                return instance_ebp.get_folders()
            except Exception as e:
                logging.warning(f"Erreur EBP: {e}")
                return []
    return []


def fetch_zeendoc_classeurs(id_client, fields):
    for field in fields:
        if field.get("TypeChamp") == "select_zeendoc_classeur":
            try:
                instance_zeendoc = zeendoc.Zeendoc(id_client)
                return instance_zeendoc.get_classeurs()
            except Exception as e:
                logging.warning(f"Erreur Zeendoc Classeur: {e}")
                return []
    return []


def fetch_zeendoc_indexes(id_client, fields):
    for field in fields:
        if field.get("TypeChamp") == "select_zeendoc_index":
            try:
                instance_zeendoc = zeendoc.Zeendoc(id_client)
                return instance_zeendoc.get_index()
            except Exception as e:
                logging.warning(f"Erreur Zeendoc Index: {e}")
                return []
    return []