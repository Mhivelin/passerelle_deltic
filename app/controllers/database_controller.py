"""
Ce module contient les routes pour les différentes entités de la base de données.
"""


from flask_jwt_extended import jwt_required
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_login import login_required
import logging
from app.models import database


# Création d'un Blueprint pour le ebp controller
database_bp = Blueprint("database", __name__)



###################################################################################################
#                                        PASSERELLE                                              #
###################################################################################################

@database_bp.route("/database/passerelle", methods=["GET"])
@login_required
def get_all_passerelles():
    """
    Obtient toutes les passerelles de la base de données.
    """
    passerelles = database.get_all_passerelles()
    return jsonify(passerelles)


@database_bp.route("/database/passerelle/<int:passerelle_id>", methods=["GET"])
@login_required
def get_passerelle_by_id(passerelle_id):
    """
    Obtient une passerelle par son ID.
    """
    passerelle = database.get_passerelle_by_id(passerelle_id)
    return jsonify(passerelle)


@database_bp.route("/database/passerelle_with_connectors/<int:passerelle_id>", methods=["GET"])
@login_required
def get_passerelle_with_connectors_by_id(passerelle_id):
    """
    Obtient une passerelle avec ses connecteurs source et destination par son ID.
    """
    passerelle = database.get_passerelle_with_connectors_by_id(passerelle_id)
    return jsonify(passerelle)



@database_bp.route("/database/passerelle", methods=["POST"])
@login_required
def add_passerelle():
    """
    Ajoute une passerelle à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter la passerelle
    database.add_passerelle(data["lib_passerelle"])
    return redirect(url_for("v_interface.home"))


@database_bp.route("/database/passerelle_with_connectors", methods=["POST"])
@login_required
def add_passerelle_with_connectors():
    """
    Ajoute une passerelle à la base de données avec un connecteur source et un connecteur destination.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter la passerelle
    database.add_passerelle_with_connectors(
        data["lib_passerelle"],
        data["id_logiciel_source"],
        data["id_logiciel_destination"]
    )
    return redirect(url_for("v_interface.home"))

@database_bp.route("/database/add_passerelle_with_connectors_and_fields", methods=["POST"])
@login_required
def add_passerelle_with_connectors_and_fields():
    """
    Ajoute une passerelle à la base de données avec un connecteur source et un connecteur destination.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
        requis_list = data['requis']
    else:
        data = request.form
        requis_list = data.getlist('requis')


    print("data: ", data)


    # ajouter la passerelle
    print("add_passerelle_with_connectors:")
    print(database.add_passerelle_with_connectors(
        data["lib_passerelle"],
        data["id_logiciel_source"],
        data["id_logiciel_destination"]))

    id_passerelle = database.get_id_passerelle_by_lib_passerelle(data["lib_passerelle"])

    # ajouter les champs
    for champ in requis_list:
        print("champ: ", champ)
        print(database.add_requiert_passerelle(champ, id_passerelle))

    return jsonify({"data": data, "requis": requis_list})
#redirect(url_for("v_interface.home"))




@database_bp.route("/database/passerelle/<int:passerelle_id>", methods=["DELETE"])
@login_required
def delete_passerelle(passerelle_id):
    """
    Supprime une passerelle de la base de données.
    """
    result = database.delete_passerelle(passerelle_id)
    return jsonify(result)



###################################################################################################
#                                        CONNECTEURS                                              #
###################################################################################################

#### CONNECTEUR SOURCE ####

@database_bp.route("/database/connecteur_source", methods=["GET"])
@login_required
def get_all_connecteurs_source():
    """
    Obtient tous les connecteurs source de la base de données.
    """
    connecteurs_source = database.get_all_connecteurs_source()
    return jsonify(connecteurs_source)



@database_bp.route("/database/connecteur_source", methods=["POST"])
@login_required
def add_connecteur_source():
    """
    Ajoute un connecteur source à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    database.add_connecteur_source(data["id_passerelle"], data["id_logiciel"])
    return redirect(url_for("v_interface.home"))

@database_bp.route("/database/connecteur_source/<int:connecteur_source_id>", methods=["GET"])
@login_required
def get_connecteur_source_by_id(connecteur_source_id):
    """
    Obtient un connecteur source par son ID.
    """
    connecteur_source = database.get_connecteur_source_by_id(connecteur_source_id)
    return jsonify(connecteur_source)


@database_bp.route("/database/connecteur_source/<int:connecteur_source_id>", methods=["DELETE"])
@login_required
def delete_connecteur_source(connecteur_source_id):
    """
    Supprime un connecteur source de la base de données.
    """
    result = database.delete_connecteur_source(connecteur_source_id)
    return jsonify(result)



#### CONNECTEUR DESTINATION ####


@database_bp.route("/database/connecteur_destination", methods=["GET"])
@login_required
def get_all_connecteurs_destination():
    """
    Obtient tous les connecteurs destination de la base de données.
    """
    connecteurs_destination = database.get_all_connecteurs_destination()
    return jsonify(connecteurs_destination)



@database_bp.route("/database/connecteur_destination", methods=["POST"])
@login_required
def add_connecteur_destination():
    """
    Ajoute un connecteur destination à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le connecteur destination
    database.add_connecteur_destination(data["id_passerelle"], data["id_logiciel"])
    return redirect(url_for("v_interface.home"))

@database_bp.route(
    "/database/connecteur_destination/<int:connecteur_destination_id>",
    methods=["GET"])
@login_required
def get_connecteur_destination_by_id(connecteur_destination_id):
    """
    Obtient un connecteur destination par son ID.
    """
    connecteur_destination = database.get_connecteur_destination_by_id(connecteur_destination_id)
    return jsonify(connecteur_destination)

@database_bp.route(
    "/database/connecteur_destination/<int:connecteur_destination_id>",
    methods=["DELETE"])
@login_required
def delete_connecteur_destination(connecteur_destination_id):
    """
    Supprime un connecteur destination de la base de données.
    """
    result = database.delete_connecteur_destination(connecteur_destination_id)
    return jsonify(result)


###################################################################################################
#                                        CLIENT                                                   #
###################################################################################################

@database_bp.route("/database/client", methods=["GET"])
@jwt_required()
def get_all_clients():
    """
    Obtient tous les clients de la base de données.
    """
    clients = database.get_all_clients()
    return jsonify(clients)


@database_bp.route("/database/client/<int:client_id>", methods=["GET"])
@login_required
def get_client_by_id(client_id):
    """
    Obtient un client par son ID.
    """
    client = database.get_client_by_id(client_id)
    return jsonify(client)


@database_bp.route("/database/client", methods=["POST"])
@login_required
def add_client():
    """
    Ajoute un client à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le client
    database.add_client(data["lib_client"])
    id_client = database.get_id_client_by_lib_client(data["lib_client"])
    return redirect(url_for("passerelle.form_connect_passerelle", idClient=id_client))


@database_bp.route("/database/app/client", methods=["POST"])
@jwt_required()
def app_add_client():
    """
    Ajoute un client à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le client
    database.add_client(data["lib_client"])
    return jsonify({"message": "Client ajouté avec succès"})


@database_bp.route("/database/client/<int:client_id>", methods=["DELETE"])
@login_required
def delete_client(client_id):
    """
    Supprime un client de la base de données.
    """
    result = database.delete_client(client_id)
    print("result: ", result)
    return jsonify(result)


###################################################################################################
#                                        LOGICIEL                                                 #
###################################################################################################

@database_bp.route("/database/logiciel", methods=["GET"])
@login_required
def get_all_logiciels():
    """
    Obtient tous les logiciels de la base de données.
    """
    logiciels = database.get_all_logiciels()
    return jsonify(logiciels)


@database_bp.route("/database/logiciel/<int:logiciel_id>", methods=["GET"])
@login_required
def get_logiciel_by_id(logiciel_id):
    """
    Obtient un logiciel par son ID.
    """
    logiciel = database.get_logiciel_by_id(logiciel_id)
    return jsonify(logiciel)


@database_bp.route("/database/logicielByPasserelle/<int:passerelle_id>", methods=["GET"])
@login_required
def get_logiciel_by_passerelle(passerelle_id):
    """
    Obtient tous les logiciels d'une passerelle.
    """
    logiciels = database.get_logiciel_by_passerelle(passerelle_id)
    return jsonify(logiciels)


@database_bp.route("/database/logiciel", methods=["POST"])
@login_required
def add_logiciel():
    """
    Ajoute un logiciel à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le logiciel
    database.add_logiciel(data["lib_logiciel"])
    return redirect(url_for("v_interface.home"))


@database_bp.route("/database/logiciel/<int:logiciel_id>", methods=["DELETE"])
@login_required
def delete_logiciel(logiciel_id):
    """
    Supprime un logiciel de la base de données.
    """
    result = database.delete_logiciel(logiciel_id)
    return jsonify(result)




###################################################################################################
#                                   CLIENT PASSERELLE                                            #
###################################################################################################

@database_bp.route("/database/client_passerelle", methods=["GET"])
@login_required
def get_all_clients_passerelle():
    """
    Obtient tous les clients passerelle de la base de données.
    """
    clients_passerelle = database.get_all_clients_passerelle()
    return jsonify(clients_passerelle)


@database_bp.route("/database/client_passerelle/<int:client_passerelle_id>", methods=["GET"])
@login_required
def get_client_passerelle_by_id(client_passerelle_id):
    """
    Obtient un client passerelle par son ID.
    """
    client_passerelle = database.get_client_passerelle_by_id(client_passerelle_id)
    return jsonify(client_passerelle)


@database_bp.route("/database/client_passerelle", methods=["POST"])
@login_required
def add_client_passerelle():
    """
    Ajoute un client passerelle à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le client passerelle
    database.add_client_passerelle(data["id_client"], data["id_passerelle"])
    return redirect(url_for("v_client.form_add_multiple_requiert", id_client=data["id_client"]))


@database_bp.route("/database/client_passerelle/<int:id_client>/<int:id_passerelle>", methods=["DELETE"])
@login_required
def delete_client_passerelle(id_client, id_passerelle):
    """
    Supprime un client passerelle de la base de données.
    """
    result = database.delete_client_passerelle(id_client, id_passerelle)
    return jsonify(result)



###################################################################################################
#                                         CHAMP                                                   #
###################################################################################################


@database_bp.route("/database/champ", methods=["GET"])
@login_required
def get_all_champs():
    """
    Obtient tous les champs de la base de données.
    """
    champs = database.get_all_champs()
    return jsonify(champs)


@database_bp.route("/database/champ/<int:champ_id>", methods=["GET"])
@login_required
def get_champ_by_id(champ_id):
    """
    Obtient un champ par son ID.
    """
    champ = database.get_champ_by_id(champ_id)
    return jsonify(champ)


@database_bp.route("/database/champ", methods=["POST"])
@login_required
def add_champ():
    """
    Ajoute un champ à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le champ
    database.add_champ(data["lib_champ"])
    return redirect(url_for("v_interface.home"))


@database_bp.route("/database/champ/<int:champ_id>", methods=["DELETE"])
@login_required
def delete_champ(champ_id):
    """
    Supprime un champ de la base de données.
    """
    result = database.delete_champ(champ_id)
    return jsonify(result)


@database_bp.route("/database/champByPasserelle/<int:passerelle_id>", methods=["GET"])
@login_required
def get_champ_by_passerelle(passerelle_id):
    """
    Obtient tous les champs d'une passerelle.
    """
    champs = database.get_champ_by_passerelle(passerelle_id)
    return jsonify(champs)


@database_bp.route("/database/champByLogiciel/<int:logiciel_id>", methods=["GET"])
@login_required
def get_champ_by_logiciel(logiciel_id):
    """
    Obtient tous les champs d'un logiciel.
    """
    champs = database.get_champ_by_logiciel(logiciel_id)
    return jsonify(champs)


@database_bp.route("/database/champByClient/<int:client_id>", methods=["GET"])
@login_required
def get_champ_by_client(client_id):
    """
    Obtient tous les champs d'un client.
    """
    champs = database.get_champ_by_client(client_id)
    return jsonify(champs)






###################################################################################################
#                                          requiert                                               #
###################################################################################################

@database_bp.route("/database/requiert", methods=["GET"])
@login_required
def get_all_requierts():
    """
    Obtient tous les requierts de la base de données.
    """
    requierts = database.get_all_requiert()
    return jsonify(requierts)


@database_bp.route("/database/requiert/<int:id_champ>/<int:id_logiciel>", methods=["GET"])
@login_required
def get_requiert_by_id(id_champ, id_logiciel):
    """
    Obtient un requiert par son ID.
    """
    requiert = database.get_requiert_by_id(id_champ, id_logiciel)
    return jsonify(requiert)

@database_bp.route("/database/logiciel_requiert", methods=["POST"])
@login_required
def add_requiert_logiciel():
    """
    Ajoute un requiert à la base de données pour un logiciel.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le requiert
    database.add_requiert_logiciel(data["id_champ"], data["id_logiciel"])
    return redirect(url_for("v_interface.home"))


@database_bp.route("/database/passerelle_requiert", methods=["POST"])
@login_required
def add_requiert_passerelle():
    """
    Ajoute un requiert à la base de données pour une passerelle.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le requiert
    database.add_requiert_passerelle(data["id_champ"], data["id_passerelle"])
    return redirect(url_for("v_interface.home"))





@database_bp.route("/database/requiert/<int:id_champ>/<int:id_logiciel>", methods=["DELETE"])
@login_required
def delete_requiert_logiciel(id_champ, id_logiciel):
    """
    Supprime un requiert de la base de données pour un logiciel.
    """
    result = database.delete_requiert_logiciel(id_champ, id_logiciel)
    return jsonify(result)


@database_bp.route("/database/requiert/<int:id_champ>/<int:id_passerelle>", methods=["DELETE"])
@login_required
def delete_requiert_passerelle(id_champ, id_passerelle):
    """
    Supprime un requiert de la base de données pour une passerelle.
    """
    result = database.delete_requiert_passerelle(id_champ, id_passerelle)
    return jsonify(result)


@database_bp.route("/database/requiertByLogiciel/<int:logiciel_id>", methods=["GET"])
@login_required
def get_requiert_by_logiciel(logiciel_id):
    """
    Obtient tous les requierts d'un logiciel.
    """
    requierts = database.get_requiert_by_logiciel(logiciel_id)
    return jsonify(requierts)


@database_bp.route("/database/requiertByPasserelle/<int:passerelle_id>", methods=["GET"])
@login_required
def get_requiert_by_passerelle(passerelle_id):
    """
    Obtient tous les requierts d'une passerelle.
    """
    requierts = database.get_requiert_by_passerelle(passerelle_id)
    return jsonify(requierts)


@database_bp.route("/database/requiertByPasserelleAndLogiciel/<int:passerelle_id>", methods=["GET"])
@login_required
def get_requiert_by_passerelle_and_his_logiciel(passerelle_id):
    """
    Obtient tous les requierts d'une passerelle et de ses logiciels.
    """
    requierts = database.get_requiert_by_passerelle_and_his_logiciel(passerelle_id)
    return jsonify(requierts)


@database_bp.route("/database/requiertByClient/<int:client_id>", methods=["GET"])
@login_required
def get_requiert_by_client(client_id):
    """
    Obtient tous les requierts d'un client (logiciels et passerelles)
    """
    requierts = database.get_requiert_by_client(client_id)
    return jsonify(requierts)



###################################################################################################
#                                     CHAMP CLIENT                                                #
###################################################################################################

@database_bp.route("/database/champ_client", methods=["GET"])
@login_required
def get_all_champs_clients():
    """
    Obtient tous les champs clients de la base de données.
    """
    champs_clients = database.get_all_champs_clients()
    return jsonify(champs_clients)


@database_bp.route("/database/champ_client/<int:champ_client_id>", methods=["GET"])
@login_required
def get_champ_client_by_id(champ_client_id):
    """
    Obtient un champ client par son ID.
    """
    champ_client = database.get_champ_client_by_id(champ_client_id)
    return jsonify(champ_client)


@database_bp.route("/database/champ_client", methods=["POST"])
@login_required
def add_champ_client():
    """
    Ajoute un champ client à la base de données.
    """
    # obtenir les données de la requête (soit en JSON, soit en form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    # ajouter le champ client
    database.add_champ_client(data["id_champ"], data["id_client"])
    return redirect(url_for("v_interface.home"))

@database_bp.route("/database/champ_client_multiple", methods=["POST"])
@login_required
def add_champ_client_multiple():
    """
    Ajoute plusieurs champs client à un client dans la base de données.
    si le champ existe déjà, il est mis à jour.
    """
    if request.is_json:
        data = request.get_json()
        id_champs = data['id_champ']
        lib_champs = data['lib_champ']
    else:
        data = request.form
        id_champs = data.getlist('id_champ[]')
        lib_champs = data.getlist('lib_champ[]')
        logging.debug("IDs: %s, Labels: %s", id_champs, lib_champs)



    # Ajouter les champs client
    id_client = data.get('id_client')
    champs = []
    for id_champ, lib_champ in zip(id_champs, lib_champs):
        database.add_champ_client(id_client, id_champ, lib_champ)
        champs.append({'id_champ': id_champ, 'lib_champ': lib_champ})

    return redirect(url_for("v_interface.home"))
    # return jsonify({"data": data, "champs": champs})


@database_bp.route("/database/champ_client_by_client/<int:client_id>", methods=["GET"])
def get_champ_client_by_client(client_id):
    """
    Obtient tous les champs d'un client.
    """
    champs = database.get_champ_client_by_client(client_id)
    return jsonify(champs)


