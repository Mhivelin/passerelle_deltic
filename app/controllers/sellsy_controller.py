"""
Ce module contient le controller pour l'API Sellsy.
"""

# from app.models.sellsy import Sellsy
from flask import Blueprint

# from requests_oauthlib import OAuth2Session

# Création d'un Blueprint pour le sellsy controller
sellsy_bp = Blueprint("sellsy", __name__)


# @sellsy_bp.route('/sellsy/callback')
# def sellsy_callback():
#     sellsy = Sellsy(client_id, client_secret, redirect_uri)
#     authorization_response = request.url
#     sellsy.fetch_token(authorization_response)
#     return "Authorization successful!"
