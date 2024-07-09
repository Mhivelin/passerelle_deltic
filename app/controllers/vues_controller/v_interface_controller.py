"""
Controlleur pour les routes des vue liées à l'interface
"""

import logging

from flask import Blueprint, render_template
from flask_login import login_required

from app.models import database  # pylint: disable=E0401

# Création d'un Blueprint pour le interface controller
v_interface_bp = Blueprint("v_interface", __name__)


@v_interface_bp.route("/")
@login_required
def home():
    """Route pour la page d'accueil avec les clients"""
    try:
        clients = database.get_all_clients()
        for client in clients:
            client["passerellesClient"] = (
                database.get_passerelle_client_with_lib_passerelle(client["IdClient"])
            )
            for passerelle in client["passerellesClient"]:
                passerelle["champs"] = (
                    database.get_champ_passerelle_client_by_ids_with_lib_champ(
                        passerelle["IdPasserelleClient"]
                    )
                )
        return render_template("clients.html", clients=clients)

    except (ValueError, KeyError, TypeError) as e:
        logging.error("An error occurred: %s", str(e))
        return str(e)
    except (database.DatabaseError, database.ConnectionError) as e:
        logging.error("A database error occurred: %s", str(e))
        return str(e), 500
    except Exception as e:  # pylint: disable=W0703
        logging.error("An unexpected error occurred: %s", str(e))
        return str(e), 500


@v_interface_bp.route("/documentation")
def documentation():
    """Route pour la documentation"""
    return render_template("documentation.html")
