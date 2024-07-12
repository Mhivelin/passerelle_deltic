"""
Ce module contient les routes pour les différentes entités de la base de données.
"""

import logging  # Le standard import doit être placé avant les imports tiers

from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.models import database  # pylint: disable=E0401

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
    except database.DatabaseError as e:
        logging.error("Error fetching clients: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error adding client: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error deleting client: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error fetching passerelles: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error adding passerelle: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route("/database/add_passerelle_with_champs", methods=["POST"])
def add_passerelle_with_champs():
    """
    Ajoute une nouvelle passerelle à la base de données avec ses champs.
    """
    lib_passerelle = request.form.get("LibPasserelle")
    id_logiciel_source = request.form.get("id_logiciel_source")
    id_logiciel_destination = request.form.get("id_logiciel_destination")
    champs = request.form.getlist("requis[]")

    try:
        # Ajouter la passerelle
        database.add_passerelle_with_logiciels(
            lib_passerelle, id_logiciel_source, id_logiciel_destination
        )

        # Récupérer l'ID de la passerelle nouvellement ajoutée
        id_passerelle = database.get_passerelle_by_lib(lib_passerelle).get(
            "IdPasserelle"
        )

        # Ajouter les champs requis
        for champ_id in champs:
            champ = database.get_champ_by_id(champ_id)
            lib_champ = champ.get("LibChamp")
            nom_table = champ.get("NomTable")
            database.add_champ(lib_champ, nom_table, id_passerelle)

        return jsonify({"message": "Passerelle added successfully"}), 201
    except database.DatabaseError as e:
        logging.error("Error adding passerelle: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error deleting passerelle: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error fetching logiciels: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error adding logiciel: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error deleting logiciel: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_logiciels_by_passerelles/<int:id_passerelle>", methods=["GET"]
)
@login_required
def get_logiciels_by_passerelles(id_passerelle):
    """
    Obtient tous les logiciels associés à une passerelle spécifique.
    """
    logiciels = database.get_logiciels_by_passerelles(id_passerelle)
    return jsonify(logiciels)


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
    except database.DatabaseError as e:
        logging.error("Error fetching champs: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_champs_by_logiciels/<int:id_logiciel>", methods=["GET"]
)
@login_required
def get_champs_by_logiciels(id_logiciel):
    """
    Obtient tous les champs associés à un logiciel spécifique.
    """
    champs = database.get_champs_by_logiciels(id_logiciel)
    return jsonify(champs)


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
    except database.DatabaseError as e:
        logging.error("Error adding champ: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error deleting champ: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error fetching connecteurs: %s", str(e))
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
            return (
                jsonify(
                    {"error": "IdLogiciel, IdPasserelle, and IsSource are required"}
                ),
                400,
            )
        database.add_connecteur(id_logiciel, id_passerelle, is_source)
        return jsonify({"message": "Connecteur added successfully"}), 201
    except database.DatabaseError as e:
        logging.error("Error adding connecteur: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/connecteur/<int:id_logiciel>/<int:id_passerelle>", methods=["DELETE"]
)
@login_required
def delete_connecteur(id_logiciel, id_passerelle):
    """
    Supprime un connecteur de la base de données par identifiant.
    """
    try:
        database.delete_connecteur(id_logiciel, id_passerelle)
        return jsonify({"message": "Connecteur deleted successfully"}), 200
    except database.DatabaseError as e:
        logging.error("Error deleting connecteur: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error fetching champ passerelles: %s", str(e))
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
            return (
                jsonify(
                    {"error": "IdPasserelleClient, IdChamp, and Valeur are required"}
                ),
                400,
            )
        database.add_champ_passerelle(id_passerelle_client, id_champ, valeur)
        return jsonify({"message": "Champ Passerelle added successfully"}), 201
    except database.DatabaseError as e:
        logging.error("Error adding champ passerelle: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/champ_passerelle/<int:id_champ>/<int:id_passerelle_client>",
    methods=["DELETE"],
)
@login_required
def delete_champ_passerelle(id_champ, id_passerelle_client):
    """
    Supprime un champ passerelle de la base de données par identifiant.
    """
    try:
        database.delete_champ_passerelle(id_champ, id_passerelle_client)
        return jsonify({"message": "Champ Passerelle deleted successfully"}), 200
    except database.DatabaseError as e:
        logging.error("Error deleting champ passerelle: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error fetching passerelle clients: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_all_passerelle_client_with_lib_passerelle", methods=["GET"]
)
@login_required
def get_all_passerelle_client_with_lib_passerelle():
    """
    Obtient toutes les passerelles client avec libellé de la passerelle.
    """
    try:
        passerelle_clients = database.get_all_passerelle_client_with_lib_passerelle()
        return jsonify(passerelle_clients)
    except database.DatabaseError as e:
        logging.error("Error fetching passerelle clients: %s", str(e))
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
    except database.DatabaseError as e:
        logging.error("Error adding passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/passerelle_client/<int:id_passerelle>/<int:id_client>",
    methods=["DELETE", "POST"],
)
@login_required
def delete_passerelle_client(id_passerelle, id_client):
    """
    Supprime une passerelle client de la base de données par identifiant.
    """
    try:
        database.delete_passerelle_client(id_passerelle, id_client)
        return jsonify({"message": "Passerelle Client deleted successfully"}), 200
    except database.DatabaseError as e:
        logging.error("Error deleting passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route("/database/passerelle_client/<int:id_client>/lib", methods=["GET"])
@login_required
def get_passerelle_client_with_lib_passerelle(id_client):
    """
    Obtient toutes les passerelles client avec libellé pour un client spécifique.
    """
    try:
        passerelle_clients = database.get_passerelle_client_with_lib_passerelle(
            id_client
        )
        return jsonify(passerelle_clients)
    except database.DatabaseError as e:
        logging.error(
            "Error fetching passerelle clients with lib passerelle: %s", str(e)
        )
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_id_passerelle_by_id_passerelle_client/<int:id_passerelle_client>",
    methods=["GET"],
)
@login_required
def get_id_passerelle_by_id_passerelle_client(id_passerelle_client):
    """
    Obtient l'ID de la passerelle par ID passerelle client.
    """
    try:
        id_passerelle = database.get_id_passerelle_by_id_passerelle_client(
            id_passerelle_client
        )
        return jsonify(id_passerelle)
    except database.DatabaseError as e:
        logging.error("Error fetching passerelle id: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route("/database/passerelle_client/<int:id_client>/champ", methods=["GET"])
@login_required
def get_champ_passerelle_client_by_client_with_lib_champ(id_client):
    """
    Obtient tous les champs passerelle client pour un client spécifique.
    """
    try:
        champ_passerelle_client = (
            database.get_champ_passerelle_client_by_client_with_lib_champ(id_client)
        )
        return jsonify(champ_passerelle_client)
    except database.DatabaseError as e:
        logging.error("Error fetching champ passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_champ_by_passerelle_and_logiciel_passerelle/<int:id_passerelle>",
    methods=["GET"],
)
@login_required
def get_champ_by_passerelle_and_logiciel_passerelle(id_passerelle):
    """
    Obtient tous les champs associés à une passerelle spécifique.
    """
    champs = database.get_champ_by_passerelle_and_logiciel_passerelle(id_passerelle)
    return jsonify(champs)


@database_bp.route("/database/add_multiple_champ_passerelle/", methods=["POST"])
@login_required
def add_multiple_champ_passerelle():
    """
    Ajoute plusieurs champs passerelle client pour un client spécifique.
    """
    try:
        data = request.form

        # Log pour déboguer le contenu de data
        logging.debug("Request data: %s", data)

        # Convertir les données du formulaire en une liste de dictionnaires
        champs = []
        id_champs = data.getlist("IdChamp[]")
        valeurs = data.getlist(
            "Valeur[]"
        )  # Assuming the values are passed in 'Valeur[]'
        id_client = data.get("id_client")
        id_passerelle = data.get("id_passerelle")
        id_passerelle_client = data.get("id_passerelle_client")

        logging.debug("id_champs: %s", id_champs)
        logging.debug("valeurs: %s", valeurs)
        logging.debug("id_client: %s", id_client)
        logging.debug("id_passerelle: %s", id_passerelle)

        if (
            not id_champs
            or not valeurs
            or not id_client
            or not id_passerelle
            or not id_passerelle_client
        ):
            return jsonify({"error": "Données manquantes"}), 400

        for id_champ, valeur in zip(id_champs, valeurs):
            champ = {"id_champ": id_champ, "Valeur": valeur}
            champs.append(champ)

        logging.debug("Champs to add: %s", champs)

        # Ajouter ou mettre à jour les champs passerelle
        database.add_or_update_champ_passerelle(id_passerelle_client, champs)

        return jsonify({"message": "Champ Passerelle ajouté avec succès"}), 201

    except database.DatabaseError as e:
        logging.error("Error adding champ passerelle: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_passerelle_client_by_ids/<int:id_passerelle>/<int:id_client>",
    methods=["GET"],
)
@login_required
def get_passerelle_client_by_ids(id_passerelle, id_client):
    """
    Obtient une passerelle client pour un client et une passerelle spécifiques.
    """
    try:
        passerelle_client = database.get_passerelle_client_by_ids(
            id_passerelle, id_client
        )
        return jsonify(passerelle_client)
    except database.DatabaseError as e:
        logging.error("Error fetching passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_champ_passerelle_client_by_passerelle_with_lib_champ/<int:id_passerelle>",
    methods=["GET"],
)
@login_required
def get_champ_passerelle_client_by_passerelle_with_lib_champ(id_passerelle):
    """
    Obtient tous les champs passerelle client pour une passerelle spécifique.
    """
    try:
        champ_passerelle_client = (
            database.get_champ_passerelle_client_by_passerelle_with_lib_champ(
                id_passerelle
            )
        )
        return jsonify(champ_passerelle_client)
    except database.DatabaseError as e:
        logging.error("Error fetching champ passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/get_champ_passerelle_client_by_ids_with_lib_champ/<int:id_passerelle>",
    methods=["GET"],
)
@login_required
def get_champ_passerelle_client_by_ids_with_lib_champ(id_passerelle):
    """
    Obtient tous les champs passerelle client pour un client et une passerelle spécifiques.
    """
    try:
        champ_passerelle_client = (
            database.get_champ_passerelle_client_by_ids_with_lib_champ(id_passerelle)
        )
        return jsonify(champ_passerelle_client)
    except database.DatabaseError as e:
        logging.error("Error fetching champ passerelle client: %s", str(e))
        return jsonify({"error": str(e)}), 500


@database_bp.route(
    "/database/reset_date_synchronisation_passerelle_client/<int:id_passerelle_client>",
    methods=["GET"],
)
@login_required
def reset_date_synchronisation_passerelle_client(id_passerelle_client):
    """
    Réinitialise la date de synchronisation de la passerelle client.
    """
    try:
        database.reset_date_synchronisation_passerelle_client(id_passerelle_client)
        return jsonify({"message": "Date de synchronisation réinitialisée avec succès"}), 200
    except database.DatabaseError as e:
        logging.error("Error resetting date synchronisation: %s", str(e))
        return jsonify({"error": str(e)}), 500