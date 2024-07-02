import os

from app.models.sellsy import Sellsy
from flask import Blueprint, jsonify, redirect, request, session, url_for
from flask_login import login_required
from requests_oauthlib import OAuth2Session

# Création d'un Blueprint pour le sellsy controller
sellsy_bp = Blueprint("sellsy", __name__)


@sellsy_bp.route('/sellsy/callback')
def sellsy_callback():
    sellsy = Sellsy(client_id='122b42fc-6463-4226-a00e-fd9ffabea442', client_secret='6fcc377c5cf41473c8afd3b68afb1fe2a55649171dadf01bb098947515c1909d', redirect_uri='http://localhost:5000/sellsy/callback')
    authorization_response = request.url
    sellsy.fetch_token(authorization_response)
    return "Authorization successful!"

