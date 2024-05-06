import os

# from app.models.database import get_db_connection
from app.models.ebp import EBP
from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_login import login_required
from requests_oauthlib import OAuth2Session

# Création d'un Blueprint pour le ebp controller
ebp_bp = Blueprint("ebp", __name__)


@ebp_bp.route("/get_folders_ebp/<id>", methods=["GET"])
@login_required
def get_folder_ebp(id):
    client = EBP(id)

    return jsonify({"folder_id": client.get_folders()})


@ebp_bp.route("/set_folder_ebp", methods=["POST"])
@login_required
def set_folder_ebp():
    data = request.get_json()
    client_id = data.get("id")
    folder_id = data.get("folder")

    print(data)

    client = EBP(client_id)
    client.setFolder(folder_id)

    return jsonify({"message": "Dossier EBP mis à jour avec succès"})


@ebp_bp.route("/login_ebp/<id>", methods=["GET"])
@login_required
def login_ebp(id):
    print("login_ebp")
    client = EBP(id)

    # Vérifier si un token valide existe déjà
    if client.is_authenticated():
        return redirect(url_for("v_interface.dashboard"))


    # Initialiser le processus OAuth si aucune session valide n'est trouvée
    redirect_uri = url_for("ebp.SignInRedirect", id=id, _external=True)
    authorization_base_url = "https://api-login.ebp.com/connect/authorize"
    scope = ["openid", "profile", "offline_access"]
    client_id = client.client_id

    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url(authorization_base_url)
    print(authorization_url)

    # Rediriger l'utilisateur vers l'URL de connexion
    return redirect(authorization_url)



@ebp_bp.route("/SignInRedirect/<id>", methods=["GET"])
def SignInRedirect(id):
    print("Redirection reçue")
    code = request.args.get("code")
    if not code:
        print("Code d'autorisation manquant")
        return redirect(url_for("v_interface.home"))  # Redirection vers une page d'erreur

    instance_client_ebp = EBP(id)
    if instance_client_ebp.callback(code, id) is None:
        print("Erreur lors de la récupération du token")
        return redirect(url_for("v_interface.home"))  # Gestion d'erreur

    # Redirigez vers une page sûre, comme le tableau de bord de l'utilisateur
    return redirect(url_for("v_interface.home"))

