"""
Ce module contient les routes pour les différentes entités de l'applications
"""

import logging
import os
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, send_file
from flask_login import login_required

from app.models import database  # pylint: disable=E0401

# Création d'un Blueprint pour le controller
main_bp = Blueprint("main", __name__)


# chemin de la base de données : instance\database.db
DATABASE_PATH = os.path.join(os.getcwd(), "instance", "database.db")


@main_bp.route("/export_db", methods=["GET"])
@login_required
def export_db():
    """
    Route pour exporter la base de données.
    """
    try:
        # Générer le nom de fichier avec la date actuelle
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"database_backup_{date_str}.db"

        # Envoyer le fichier
        response = send_file(DATABASE_PATH, as_attachment=True)

        # Modifier les en-têtes pour définir le nom de fichier de l'attachement
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    except FileNotFoundError as e:
        logging.error("Database file not found: %s", str(e))
        return jsonify({"success": False, "message": "Database file not found"}), 404
    except PermissionError as e:
        logging.error("Permission error: %s", str(e))
        return jsonify({"success": False, "message": "Permission error"}), 403
    except Exception as e:  # pylint: disable=W0703
        logging.error("Unexpected error: %s", str(e))
        return jsonify({"success": False, "message": str(e)}), 500


@main_bp.route("/import_db", methods=["POST", "GET"])
@login_required
def import_db():
    """
    Route pour importer la base de données.
    """
    if request.method == "GET":
        return render_template("import_db.html")

    try:
        file = request.files["file"]
        file.save(DATABASE_PATH)
        database.create_database()
        return jsonify({"success": True, "message": "Importation réussie"})
    except FileNotFoundError as e:
        logging.error("File not found: %s", str(e))
        return jsonify({"success": False, "message": "File not found"}), 404
    except PermissionError as e:
        logging.error("Permission error: %s", str(e))
        return jsonify({"success": False, "message": "Permission error"}), 403
    except Exception as e:  # pylint: disable=W0703
        logging.error("Unexpected error: %s", str(e))
        return jsonify({"success": False, "message": str(e)}), 500


@main_bp.route("/parametres", methods=["GET"])
@login_required
def parametres():
    """
    Route pour afficher les paramètres
    """
    return render_template("parametres.html")
