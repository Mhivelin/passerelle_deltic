"""
Ce module contient les routes pour les différentes entités de l'applications
"""

from flask import Blueprint, send_file, request, render_template, jsonify
from flask_login import login_required
import os
import logging
from datetime import datetime
from app.models import database

# Création d'un Blueprint pour le controller
main_bp = Blueprint("main", __name__)


# chemin de la base de données : instance\database.db
DATABASE_PATH = os.path.join(os.getcwd(), "instance", "database.db")

@main_bp.route("/export_db", methods=["GET"])
@login_required
def export_db():
    try:
        # Générer le nom de fichier avec la date actuelle
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"database_backup_{date_str}.db"

        # Envoyer le fichier
        response = send_file(DATABASE_PATH, as_attachment=True)

        # Modifier les en-têtes pour définir le nom de fichier de l'attachement
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response
    except Exception as e:
        return str(e), 500

@main_bp.route("/import_db", methods=["POST", "GET"])
@login_required
def import_db():
    if request.method == "GET":
        return render_template("import_db.html")

    try:
        file = request.files["file"]
        file.save(DATABASE_PATH)
        database.create_database()
        return jsonify({"success": True, "message": "Importation réussie"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



@main_bp.route("/parametres", methods=["GET"])
@login_required
def parametres():
    return render_template("parametres.html")


