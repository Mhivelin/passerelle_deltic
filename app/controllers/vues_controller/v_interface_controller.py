"""
Controlleur pour les routes des vue liées à l'interface
"""

from flask import Blueprint, render_template
from flask_login import login_required
from app.models import database


# Création d'un Blueprint pour le interface controller
v_interface_bp = Blueprint("v_interface", __name__)

@v_interface_bp.route("/")
@login_required
def home():

    clients = database.get_all_clients()

    for client in clients:
        client["passerellesClient"] = database.get_passerelle_client_by_client(client["idClient"])
        client["champsClient"] = database.get_champ_client_by_client(client["idClient"])

    return render_template("clients.html", clients=clients)


@v_interface_bp.route("/documentation")
def documentation():
    return render_template("documentation.html")