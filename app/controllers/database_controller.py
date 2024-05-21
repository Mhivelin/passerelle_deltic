"""
Ce module contient les routes pour les différentes entités de la base de données.
"""

from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_login import login_required
import logging
from app.models import database

# Création d'un Blueprint pour le controller
database_bp = Blueprint("database", __name__)

###################################################################################################
#                                        CLIENT                                                  #
###################################################################################################

@database_bp.route("/database/client", methods=["GET"])
@login_required
def get_all_clients():
    """
    Obtient tous les clients de la base de données.
    """
    try:
        clients = database.get_all_clients()
        return jsonify(clients)
    except Exception as e:
        logging.error(f"Error fetching clients: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/client", methods=["POST"])
@login_required
def add_client():
    """
    Ajoute un nouveau client à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        username = data.get("username")
        if not username:
            return jsonify({"error": "Username is required"}), 400
        database.add_client(username)
        return jsonify({"message": "Client added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding client: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/client/<int:id_client>", methods=["DELETE"])
@login_required
def delete_client(id_client):
    """
    Supprime un client de la base de données par identifiant.
    """
    try:
        database.delete_client(id_client)
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting client: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        PASSERELLE                                              #
###################################################################################################

@database_bp.route("/database/passerelle", methods=["GET"])
@login_required
def get_all_passerelles():
    """
    Obtient toutes les passerelles de la base de données.
    """
    try:
        passerelles = database.get_all_passerelles()
        return jsonify(passerelles)
    except Exception as e:
        logging.error(f"Error fetching passerelles: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/passerelle", methods=["POST"])
@login_required
def add_passerelle():
    """
    Ajoute une nouvelle passerelle à la base de données.
    """

    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        lib_passerelle = data.get("LibPasserelle")
        if not lib_passerelle:
            return jsonify({"error": "LibPasserelle is required"}), 400
        database.add_passerelle(lib_passerelle)
        return jsonify({"message": "Passerelle added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding passerelle: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/passerelle/<int:id_passerelle>", methods=["DELETE"])
@login_required
def delete_passerelle(id_passerelle):
    """
    Supprime une passerelle de la base de données par identifiant.
    """
    try:
        database.delete_passerelle(id_passerelle)
        return jsonify({"message": "Passerelle deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting passerelle: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        LOGICIEL                                                #
###################################################################################################

@database_bp.route("/database/logiciel", methods=["GET"])
@login_required
def get_all_logiciels():
    """
    Obtient tous les logiciels de la base de données.
    """
    try:
        logiciels = database.get_all_logiciels()
        return jsonify(logiciels)
    except Exception as e:
        logging.error(f"Error fetching logiciels: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/logiciel", methods=["POST"])
@login_required
def add_logiciel():
    """
    Ajoute un nouveau logiciel à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        lib_logiciel = data.get("lib_logiciel")
        if not lib_logiciel:
            return jsonify({"error": "LibLogiciel is required"}), 400
        database.add_logiciel(lib_logiciel)
        return jsonify({"message": "Logiciel added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding logiciel: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/logiciel/<int:id_logiciel>", methods=["DELETE"])
@login_required
def delete_logiciel(id_logiciel):
    """
    Supprime un logiciel de la base de données par identifiant.
    """
    try:
        database.delete_logiciel(id_logiciel)
        return jsonify({"message": "Logiciel deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting logiciel: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        CHAMPS                                                  #
###################################################################################################

@database_bp.route("/database/champ", methods=["GET"])
@login_required
def get_all_champs():
    """
    Obtient tous les champs de la base de données.
    """
    try:
        champs = database.get_all_champs()
        return jsonify(champs)
    except Exception as e:
        logging.error(f"Error fetching champs: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/champ", methods=["POST"])
@login_required
def add_champ():
    """
    Ajoute un nouveau champ à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        lib_champ = data.get("lib_champ")
        nom_table = data.get("nom_table")
        id_passerelle = data.get("id_passerelle")
        id_logiciel = data.get("id_logiciel")
        if not lib_champ or not nom_table:
            return jsonify({"error": "LibChamp and NomTable are required"}), 400
        database.add_champ(lib_champ, nom_table, id_passerelle, id_logiciel)
        return jsonify({"message": "Champ added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding champ: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/champ/<int:id_champ>", methods=["DELETE"])
@login_required
def delete_champ(id_champ):
    """
    Supprime un champ de la base de données par identifiant.
    """
    try:
        database.delete_champ(id_champ)
        return jsonify({"message": "Champ deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting champ: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        CONNECT_LOGICIEL                                        #
###################################################################################################

@database_bp.route("/database/connecteur", methods=["GET"])
@login_required
def get_all_connecteurs():
    """
    Obtient tous les connecteurs de la base de données.
    """
    try:
        connecteurs = database.get_all_connecteurs()
        return jsonify(connecteurs)
    except Exception as e:
        logging.error(f"Error fetching connecteurs: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/connecteur", methods=["POST"])
@login_required
def add_connecteur():
    """
    Ajoute un nouveau connecteur à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        id_logiciel = data.get("id_logiciel")
        id_passerelle = data.get("id_passerelle")
        is_source = data.get("is_source")
        if not id_logiciel or not id_passerelle or is_source is None:
            return jsonify({"error": "IdLogiciel, IdPasserelle, and IsSource are required"}), 400
        database.add_connecteur(id_logiciel, id_passerelle, is_source)
        return jsonify({"message": "Connecteur added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding connecteur: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/connecteur/<int:id_logiciel>/<int:id_passerelle>", methods=["DELETE"])
@login_required
def delete_connecteur(id_logiciel, id_passerelle):
    """
    Supprime un connecteur de la base de données par identifiant.
    """
    try:
        database.delete_connecteur(id_logiciel, id_passerelle)
        return jsonify({"message": "Connecteur deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting connecteur: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        CHAMP_PASSERELLE                                        #
###################################################################################################

@database_bp.route("/database/champ_passerelle", methods=["GET"])
@login_required
def get_all_champ_passerelle():
    """
    Obtient tous les champs passerelle de la base de données.
    """
    try:
        champ_passerelles = database.get_all_champ_passerelle()
        return jsonify(champ_passerelles)
    except Exception as e:
        logging.error(f"Error fetching champ passerelles: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/champ_passerelle", methods=["POST"])
@login_required
def add_champ_passerelle():
    """
    Ajoute un nouveau champ passerelle à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        id_passerelle_client = data.get("id_passerelle_client")
        id_champ = data.get("id_champ")
        valeur = data.get("valeur")
        if not id_passerelle_client or not id_champ or not valeur:
            return jsonify({"error": "IdPasserelleClient, IdChamp, and Valeur are required"}), 400
        database.add_champ_passerelle(id_passerelle_client, id_champ, valeur)
        return jsonify({"message": "Champ Passerelle added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding champ passerelle: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/champ_passerelle/<int:id_champ>/<int:id_passerelle_client>", methods=["DELETE"])
@login_required
def delete_champ_passerelle(id_champ, id_passerelle_client):
    """
    Supprime un champ passerelle de la base de données par identifiant.
    """
    try:
        database.delete_champ_passerelle(id_champ, id_passerelle_client)
        return jsonify({"message": "Champ Passerelle deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting champ passerelle: {e}")
        return jsonify({"error": str(e)}), 500

###################################################################################################
#                                        PASSERELLE_CLIENT                                       #
###################################################################################################

@database_bp.route("/database/passerelle_client", methods=["GET"])
@login_required
def get_all_passerelle_client():
    """
    Obtient toutes les passerelles client de la base de données.
    """
    try:
        passerelle_clients = database.get_all_passerelle_client()
        return jsonify(passerelle_clients)
    except Exception as e:
        logging.error(f"Error fetching passerelle clients: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/passerelle_client", methods=["POST"])
@login_required
def add_passerelle_client():
    """
    Ajoute une nouvelle passerelle client à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        id_passerelle = data.get("id_passerelle")
        id_client = data.get("id_client")
        if not id_passerelle or not id_client:
            return jsonify({"error": "IdPasserelle and IdClient are required"}), 400
        database.add_passerelle_client(id_passerelle, id_client)
        return jsonify({"message": "Passerelle Client added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding passerelle client: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/passerelle_client/<int:id_passerelle>/<int:id_client>", methods=["DELETE"])
@login_required
def delete_passerelle_client(id_passerelle, id_client):
    """
    Supprime une passerelle client de la base de données par identifiant.
    """
    try:
        database.delete_passerelle_client(id_passerelle, id_client)
        return jsonify({"message": "Passerelle Client deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting passerelle client: {e}")
        return jsonify({"error": str(e)}), 500

@database_bp.route("/database/passerelle_client/<int:id_client>/lib", methods=["GET"])
@login_required
def get_passerelle_client_with_lib_passerelle(id_client):
    """
    Obtient toutes les passerelles client avec libellé pour un client spécifique.
    """
    try:
        passerelle_clients = database.get_passerelle_client_with_lib_passerelle(id_client)
        return jsonify(passerelle_clients)
    except Exception as e:
        logging.error(f"Error fetching passerelle clients with lib passerelle: {e}")
        return jsonify({"error": str(e)}), 500



@database_bp.route("/database/passerelle_client/<int:id_client>/champ", methods=["GET"])
@login_required
def get_champ_passerelle_client_by_client_with_lib_champ(id_client):
    """
    Obtient tous les champs passerelle client pour un client spécifique.
    """
    try:
        champ_passerelle_client = database.get_champ_passerelle_client_by_client_with_lib_champ(id_client)
        return jsonify(champ_passerelle_client)
    except Exception as e:
        logging.error(f"Error fetching champ passerelle client: {e}")
        return jsonify({"error": str(e)}), 500



@database_bp.route("/database/add_multiple_champ_passerelle/", methods=["POST"])
@login_required
def add_multiple_champ_passerelle():
    """
    Ajoute plusieurs champs passerelle client pour un client spécifique.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        for champ in data:
            id_champ = champ.get("id_champ")
            valeur = champ.get("valeur")
            id_client = champ.get("id_client")
            if not id_champ or not valeur:
                return jsonify({"error": "IdChamp and Valeur are required"}), 400
            database.add_champ_passerelle(id_client, id_champ, valeur)
        return jsonify({"message": "Champ Passerelle added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding champ passerelle: {e}")
        return jsonify({"error": str(e)}), 500



###################################################################################################
#                                       application controller                                    #
###################################################################################################

@database_bp.route("/database/app/client", methods=["GET"])
@jwt_required()
def get_all_clients_app():
    """
    Obtient tous les clients de la base de données.
    """
    try:
        clients = database.get_all_clients()
        return jsonify(clients)
    except Exception as e:
        logging.error(f"Error fetching clients: {e}")
        return jsonify({"error": str(e)}), 500


@database_bp.route("/database/app/client", methods=["POST"])
@jwt_required()
def add_client_app():
    """
    Ajoute un nouveau client à la base de données.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        username = data.get("username")
        if not username:
            return jsonify({"error": "Username is required"}), 400
        database.add_client(username)
        return jsonify({"message": "Client added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding client: {e}")
        return jsonify({"error": str(e)}), 500

# get_all_logiciels
@database_bp.route("/database/app/logiciel", methods=["GET"])
@jwt_required()
def get_all_logiciels_app():
    """
    Obtient tous les logiciels de la base de données.
    """
    try:
        logiciels = database.get_all_logiciels()
        return jsonify(logiciels)
    except Exception as e:
        logging.error(f"Error fetching logiciels: {e}")
        return jsonify({"error": str(e)}), 500


# get_all_champs
@database_bp.route("/database/app/champ", methods=["GET"])
@jwt_required()
def get_all_champs_app():
    """
    Obtient tous les champs de la base de données.
    """
    try:
        champs = database.get_all_champs()
        return jsonify(champs)
    except Exception as e:
        logging.error(f"Error fetching champs: {e}")
        return jsonify({"error": str(e)}), 500

# add_passerelle
@database_bp.route("/database/app/passerelle", methods=["POST"])
@jwt_required()
def add_passerelle_app():
    """
    Ajoute une nouvelle passerelle à la base de données.
    """

    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        lib_passerelle = data.get("LibPasserelle")
        if not lib_passerelle:
            return jsonify({"error": "LibPasserelle is required"}), 400
        database.add_passerelle(lib_passerelle)
        return jsonify({"message": "Passerelle added successfully"}), 201
    except Exception as e:
        logging.error(f"Error adding passerelle: {e}")
        return jsonify({"error": str(e)}), 500