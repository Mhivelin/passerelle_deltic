"""
Ce fichier contient les routes pour les clients
"""


# import json
# import sqlite3
from flask import Blueprint, redirect, request
from flask_login import login_required

# from app.models.database import get_db_connection
from app.models.client import Client    # pylint: disable=E0401

# from app.models import database

# Création d'un Blueprint pour le client controller
client_bp = Blueprint("client", __name__)




# route pour récupérer les données d'un client par son id
# @client_bp.route("/client", methods=["GET"])
# @login_required
# def get_client():
#     """
#     Route pour récupérer les données d'un client par son id
#     """
#     client_id = request.args.get("id")
#     client = client(client_id)

#     ebp = client.clientEBP.BdGetClientEBP(client_id)
#     zeendoc = client.clientZeendoc.BdGetClientZeendoc(client_id)

#     return jsonify({"clientId": client_id, "ebp": ebp, "zeendoc": zeendoc})



@client_bp.route("/launch_routine", methods=["POST"])
@login_required
def launch_routine():
    """
    Route pour lancer la routine d'un client
    """
    client_id = request.form.get("client_id")
    client = Client(client_id)
    client.routine()
    return redirect("/")
