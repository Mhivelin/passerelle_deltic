"""
Ce fichier contient les fonctions de contrôle pour les actions liées à l'ERP EBP.
"""

# import os

from flask import Blueprint, jsonify, redirect, request, url_for
from flask_login import login_required
from requests_oauthlib import OAuth2Session

# from app.models.database import get_db_connection
from app.models.ebp import EBP  # pylint: disable=E0401

# Création d'un Blueprint pour le ebp controller
ebp_bp = Blueprint("ebp", __name__)


@ebp_bp.route("/get_folders_ebp/<IdPasserelleClient>", methods=["GET"])
@login_required
def get_folder_ebp(IdPasserelleClient):
    """
    Route pour récupérer les dossiers de l'ERP EBP
    """
    client = EBP(IdPasserelleClient)

    return jsonify({"folder_id": client.get_folders()})


@ebp_bp.route("/set_folder_ebp", methods=["POST"])
@login_required
def set_folder_ebp():
    """
    Route pour mettre à jour le dossier
    """
    data = request.get_json()
    client_id = data.get("id")
    folder_id = data.get("folder")

    print(data)

    client = EBP(client_id)
    client.setFolder(folder_id)

    return jsonify({"message": "Dossier EBP mis à jour avec succès"})


@ebp_bp.route("/login_ebp/<IdPasserelleClient>", methods=["GET"])
@login_required
def login_ebp(IdPasserelleClient):
    """
    Route pour gérer la connexion à l'ERP EBP
    """
    print("login_ebp")
    client = EBP(IdPasserelleClient)

    # Vérifier si un token valide existe déjà
    if client.is_authenticated():
        return redirect(url_for("v_interface.home"))

    # Initialiser le processus OAuth si aucune session valide n'est trouvée
    redirect_uri = url_for(
        "ebp.SignInRedirect", IdPasserelleClient=IdPasserelleClient, _external=True
    )
    authorization_base_url = "https://api-login.ebp.com/connect/authorize"
    scope = ["openid", "profile", "offline_access"]
    client_id = client.client_id

    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url(
        authorization_base_url
    )  # pylint: disable=W0612
    print(authorization_url)

    # Rediriger l'utilisateur vers l'URL de connexion
    return redirect(authorization_url)


@ebp_bp.route("/SignInRedirect/<IdPasserelleClient>", methods=["GET"])
def SignInRedirect(IdPasserelleClient):
    """
    Route pour gérer la redirection après la connexion à l'ERP EBP
    """
    print("Redirection reçue")
    code = request.args.get("code")
    if not code:
        print("Code d'autorisation manquant")
        return redirect(
            url_for("v_interface.home")
        )  # Redirection vers une page d'erreur

    instance_client_ebp = EBP(IdPasserelleClient)
    if instance_client_ebp.callback(code, IdPasserelleClient) is None:
        print("Erreur lors de la récupération du token")
        return redirect(url_for("v_interface.home"))  # Gestion d'erreur

    # Redirigez vers une page sûre, comme le tableau de bord de l'utilisateur
    return redirect(url_for("v_interface.home"))
