import json
import sys
import datetime
import urllib.parse

import requests
from requests.exceptions import HTTPError
from flask import jsonify, url_for
import time
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError, BackendApplicationClient
from requests_oauthlib import OAuth2Session
from app.models import database as db

import app.models.database as db


class EBP:
    """
    Classe qui permet de gérer les interactions avec l'API EBP.
    """

    def __init__(self, id) -> None:
        """ Constructeur de la classe EBP. """

        self.databaseId = id
        infos = db.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(id)


        for info in infos:
            if info["LibChamp"] == "EBP_Client_ID":
                print("Client ID:", info["Valeur"])
                self.client_id = info["Valeur"]
            elif info["LibChamp"] == "EBP_Client_Secret":
                print("Client Secret:", info["Valeur"])
                self.client_secret = info["Valeur"]
            elif info["LibChamp"] == "EBP_Subscription_Key":
                print("Subscription Key:", info["Valeur"])
                self.ebp_subscription_key = info["Valeur"]
            elif info["LibChamp"] == "EBP_FOLDER_ID":
                print("Folder ID:", info["Valeur"])
                self.folder_id = info["Valeur"]
            elif info["LibChamp"] == "EBP_token":
                print("Token:", info["Valeur"])
                self.token = json.loads(info["Valeur"])
                self.refresh_token_value = self.token["refresh_token"]

    def validate_token(self, token):
        """Valide si le token est encore valide."""
        valeur = token.get('Valeur')
        if not valeur:
            print("Le token n'a pas de champ 'Valeur' !!!!!!!!!!!!!!!!!")
            return False

        valeur_dict = json.loads(valeur)
        expiration = valeur_dict.get("expires_at")
        if expiration is None:
            print("Le champ 'expires_at' n'est pas présent dans le token !!!!!!!!!!!!!!!!!")
            return False

        now = datetime.datetime.now().timestamp()
        if expiration < now:
            print("Le token a expiré !!!!!!!!!!!!!!!!!")
            return False
        return True

    def is_authenticated(self):
        token = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(self.databaseId, "EBP_token")
        if token and self.validate_token(token):
            return True
        return False

    def refresh_token(self):
        url = "https://api-login.ebp.com/connect/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token_value
        }

        try:
            response = requests.post(url, headers=headers, data=urllib.parse.urlencode(body))

            if response.status_code == 200:
                new_token = response.json()
                self.Bdtoken_saver(new_token)
                return new_token
            else:
                print(f"Failed to refresh token. Status Code: {response.status_code}")
                print(f"Response Text: {response.text}")
                print(f"Request Body: {body}")
                print(f"Request Headers: {headers}")
                response.raise_for_status()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

    def login(self):
        print("Début du login")
        authorization_base_url = 'https://api-login.ebp.com/connect/authorize'
        token_url = 'https://api-login.ebp.com/connect/token'
        redirect_uri = url_for('ebp.SignInRedirect', id=self.client_id, _external=True)
        scope = ["openid", "profile", "offline_access"]

        token = None

        try:
            token = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(self.databaseId, "EBP_token")
        except Exception as e:
            print("Erreur lors de la récupération du token de la base de données:", e)

        if not token:
            oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri, scope=scope)
            authorization_url, state = oauth.authorization_url(authorization_base_url)
            print('Aller à %s et autoriser l\'accès.' % authorization_url)
            authorization_response = input('Entrez l\'URL de redirection: ')
            token = oauth.fetch_token(token_url, authorization_response=authorization_response, client_secret=self.client_secret)
            if token:
                self.Bdtoken_saver(token)
        elif not self.validate_token(token):
            print("Le token est invalide, rafraîchissement...")
            token = self.refresh_token()

        self.token = token
        return token

    def callback(self, code, IdClient):
        print("Début du callback")
        redirect_uri = url_for("ebp.SignInRedirect", id=IdClient, _external=True)
        token_url = "https://api-login.ebp.com/connect/token"

        try:
            oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri)
            token = oauth.fetch_token(token_url, client_secret=self.client_secret, code=code)
            if token:
                print(f"Token récupéré avec succès : {token}")
            else:
                print("Aucun token récupéré")

            self.Bdtoken_saver(token)


            return self.create_oauth_session(token)
        except Exception as e:
            print("Erreur lors de l'échange du code d'autorisation:", e)
            return None

    def create_oauth_session(self, token):
        token_url = "https://api-login.ebp.com/connect/token"
        return OAuth2Session(
            self.client_id,
            token=token,
            auto_refresh_kwargs={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            auto_refresh_url=token_url,
            token_updater=self.Bdtoken_saver,
        )

    def Bdtoken_saver(self, token):
        print("Début de l'enregistrement du token")
        token_json = json.dumps(token)

        # on vérifie si le token existe déjà
        token_db = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(self.databaseId, "EBP_token")
        print("Token de la base de données:", token_db)
        if token_db:
            try:
                idChamp = db.get_id_champ_by_lib_champ("EBP_token")
                db.update_champ_passerelle(self.databaseId, idChamp, token_json)
                print("Token mis à jour avec succès.")
            except Exception as e:
                print("Erreur lors de la mise à jour du token:", e)


        else:
            try:
                idChamp = db.get_id_champ_by_lib_champ("EBP_token")
                db.add_champ_passerelle(self.databaseId, idChamp, token_json)
                print("Token enregistré avec succès.")
            except Exception as e:
                print("Erreur lors de l'enregistrement du token:", e)

    def make_request(self, method, url, headers=None, params=None, data=None):
        self.login()

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if data is None:
            data = {}



        access_token = self.token["Valeur"]
        access_token = json.loads(access_token)
        access_token = access_token["access_token"]
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        else:
            raise ValueError("Access token is missing or expired")

        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response

    def get_folders(self):
        url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders?Offset=0&Limit=100&Accept-Language=fr-FR"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)
        res = response.text
        res = json.loads(res)
        res = res["folders"]
        return res

    def get_suppliers(self):
        url = f"https://api-developpeurs.ebp.com/gescom/api/v1/Folders/{self.folder_id}/GenericQuery?TableName=supplier&Columns=name, Id&=2020-11-06"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)
        return response.text

    def get_paid_documents(self):
        url = f"https://api-developpeurs.ebp.com/gescom/api/v1/Folders/{self.folder_id}/Documents/PurchaseDocument?Duration=30&DocumentType=null&ToDate=1999-01-01&Columns=DocumentNumber, Reference, CommitmentsBalanceDue&WhereCondition=%20%20type%3A%20CustomFilter%0A%20%20column%3A%20CommitmentsBalanceDue%0A%20%20operator%3A%20Equal%0A%20%20valueType%20%3A%20Decimal%0A%20%20value%3A%0A%20%20-%200"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)
        return response.text
