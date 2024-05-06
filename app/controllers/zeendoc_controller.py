# from app.models.database import get_db_connection
from app.models.zeendoc import Zeendoc
from flask import Blueprint, jsonify, redirect, render_template, request
from flask_login import login_required

# Création d'un Blueprint pour le zeendoc controller
zeendoc_bp = Blueprint("zeendoc", __name__)


@zeendoc_bp.route("/get_classeurs_zeendoc/<int:id>", methods=["GET"])
@login_required
def get_classeurs_zendoc(id):
    client = Zeendoc(id)
    classeurs = client.get_rights()["Collections"]

    return jsonify(classeurs)





