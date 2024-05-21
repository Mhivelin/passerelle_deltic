import json
import sys
import requests
from flask import jsonify, url_for
import time
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError
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


        infos = db.get_champ_client_by_client(id)


        # infos = [{"IdClient":1,"id_champ":1,"lib_champ":"EBP_Client_ID","nomTable":"EBP","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":2,"lib_champ":"EBP_Client_Secret","nomTable":"EBP","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":3,"lib_champ":"EBP_Subscription_Key","nomTable":"EBP","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":4,"lib_champ":"Zeendoc_Login","nomTable":"Zeendoc","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":5,"lib_champ":"Zeendoc_URL_Client","nomTable":"Zeendoc","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":6,"lib_champ":"Zeendoc_CPassword","nomTable":"Zeendoc","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":7,"lib_champ":"EBP_FOLDER_ID","nomTable":"remont\u00e9e de paiement","valeur":"/database/champ_client_by_client/"},{"IdClient":1,"id_champ":8,"lib_champ":"Zeendoc_CLASSEUR","nomTable":"remont\u00e9e de paiement","valeur":"/database/champ_client_by_client/"}]

        for info in infos:
            if info["lib_champ"] == "EBP_Client_ID":
                self.client_id = info["valeur"]
            elif info["lib_champ"] == "EBP_Client_Secret":
                self.client_secret = info["valeur"]
            elif info["lib_champ"] == "EBP_Subscription_Key":
                self.ebp_subscription_key = info["valeur"]
            elif info["lib_champ"] == "EBP_FOLDER_ID":
                self.folder_id = info["valeur"]
            elif info["lib_champ"] == "EBP_token":
                self.token = json.loads(info["valeur"])
            elif info["lib_champ"] == "EBP_token":
                self.token = json.loads(info["valeur"])






        # login = self.login()
        # print('login test')
        # print(login)


    def validate_token(self, token):
        """Valide si le token est encore valide."""
        expiration_timestamp = token.get("expires_at")
        if not expiration_timestamp:
            return False  # Le token ne contient pas d'informations d'expiration, considéré comme invalide
        current_timestamp = time.time()
        return current_timestamp < expiration_timestamp



    def is_authenticated(self):
        # Pseudo-code pour vérifier si le token est valide
        token = db.get_champ_client_by_label("EBP_token", self.databaseId)
        if token and self.validate_token(token):
            return True
        return False


    def refresh_token(self):
        """Rafraîchit le token d'accès."""
        token = db.get_champ_client_by_label("EBP_token", self.databaseId)
        if not token:
            return False
        try:
            # print("Rafraîchissement du token")
            # print("client_id : ", self.client_id)
            oauth = OAuth2Session(self.client_id, token=token)
            new_token = oauth.refresh_token("https://api-login.ebp.com/connect/token", client_id=self.client_id, client_secret=self.client_secret)
            if new_token:
                self.Bdtoken_saver(new_token)
                return True
            return False
        except InvalidClientError as e:
            print("Erreur de rafraîchissement du token:", e)
            return False
        except TokenExpiredError as e:
            print("Le token a expiré:", e)
            return False

    def login(self):
        print("Début du login")
        authorization_base_url = 'https://api-login.ebp.com/connect/authorize'
        token_url = 'https://api-login.ebp.com/connect/token'
        redirect_uri = url_for('ebp.SignInRedirect', id=self.client_id, _external=True)
        scope = ["openid", "profile", "offline_access"]

        try:
            token = db.get_champ_client_by_label("EBP_token", self.databaseId)
        except Exception as e:
            print("Erreur lors de la récupération du token de la base de données:", e)

        if not token :
            oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri, scope=scope)
            authorization_url, state = oauth.authorization_url(authorization_base_url)
            print('Aller à %s et autoriser l\'accès.' % authorization_url)
            authorization_response = input('Entrez l\'URL de redirection: ')
            token = oauth.fetch_token(token_url, authorization_response=authorization_response, client_secret=self.client_secret)
            if token:
                self.Bdtoken_saver(token)

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

            idChamp = db.get_id_champ_by_lib_champ("EBP_token")
            print("token : ", token)
            db.add_champ_client(IdClient, idChamp, token)
            print("Token enregistré avec succès.")
            return self.create_oauth_session(token)

        except Exception as e:
            print("Erreur lors de l'échange du code d'autorisation:", e)
            return None


    def create_oauth_session(self, token):
        """Crée et renvoie une session OAuth avec le token fourni."""
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
        token_json = json.dumps(token)
        try:
            idChamp = db.get_id_champ_by_lib_champ("EBP_token")
            db.add_champ_client(self.databaseId, idChamp, token_json)
            print("Token enregistré avec succès.")
        except Exception as e:
            print("Erreur lors de l'enregistrement du token:", e)



    def make_request(self, method, url, headers=None, params=None, data=None):
        """
        Fonction générique pour effectuer des requêtes HTTP.
        Args:
            method (str): Méthode HTTP (GET, POST, etc.)
            url (str): URL complète de la requête
            headers (dict, optional): En-têtes HTTP
            params (dict, optional): Paramètres de l'URL
            data (dict, optional): Données à envoyer dans le corps de la requête
        Returns:
            response (requests.Response): Réponse de la requête
        """

        self.login()

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if data is None:
            data = {}


        access_token = self.token["valeur"]
        # on transforme le token en json
        access_token = json.loads(access_token)
        access_token = access_token["access_token"]
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        else:
            raise ValueError("Access token is missing or expired")

        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response


    def get_folders(self):
        """
        Fonction qui permet de récupérer les dossiers de l'API EBP.
        Returns:
            response (str): Réponse textuelle de l'API
        """
        url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders?Offset=0&Limit=100&Accept-Language=fr-FR"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)
        res = response.text
        # transforme en json
        res = json.loads(res)
        res = res["folders"]

        return res





    def get_suppliers(self):
        """
        "https://api-developpeurs.ebp.com/gescom/api/v1/Folders/306851/GenericQuery?TableName=supplier&Columns=name, Id&=2020-11-06"
        Fonction qui permet de récupérer les fournisseurs de l'API EBP.
        """
        url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders/" + self.folder_id + "/GenericQuery?TableName=supplier&Columns=name, Id&=2020-11-06"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)

        return response.text



# url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders/306851/Documents/PurchaseDocument?Duration=30&DocumentType=null&ToDate=1999-01-01&Columns=DocumentNumber, Reference, CommitmentsBalanceDue&WhereCondition=%20%20type%3A%20CustomFilter%0A%20%20column%3A%20CommitmentsBalanceDue%0A%20%20operator%3A%20Equal%0A%20%20valueType%20%3A%20Decimal%0A%20%20value%3A%0A%20%20-%200"

# payload = {}
# headers = {
#   'ebp-subscription-key': '9b90dc6db6554429a027cb43fe12ab4e',
#   'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjVDNzI4RTIxOTYwQURBODdCQkQ5M0I5QTgwNjgxRURFRjhFRkI5QTQiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJYSEtPSVpZSzJvZTcyVHVhZ0dnZTN2anZ1YVEifQ.eyJuYmYiOjE3MTQ3MjMxOTYsImV4cCI6MTcxNDcyNjc5NiwiaXNzIjoiaHR0cHM6Ly9hcGktbG9naW4uZWJwLmNvbSIsImNsaWVudF9pZCI6Imp1cGl0ZXJ3aXRob3V0cGtjZSIsInN1YiI6IjRjOTUxZGI2LWM5MTQtNGYxNS05ZmQwLTE5OGJjZDQzYTY4OCIsImF1dGhfdGltZSI6MTcxNDY1MjU3OSwiaWRwIjoiRWJwTG9naW5WMiIsImVicC5lbWFpbCI6Im1hcml1cy5oaXZlbGluQGdtYWlsLmNvbSIsIm5hbWUiOiJNYXJpdXMgSGl2ZWxpbiIsInNfaGFzaCI6InhJZU81R3VWV2o2R1Z6dHhJeG93MGciLCJmYW1pbHlfbmFtZSI6IkhpdmVsaW4iLCJnaXZlbl9uYW1lIjoiTWFyaXVzIiwiZW1haWwiOiJtYXJpdXMuaGl2ZWxpbkBnbWFpbC5jb20iLCJodHRwOi8vbG9naW4uc2NoZW1hcy5lYnAuY29tL2lkZW50aXR5L2NsYWltcy9Db2RlVGllcnMiOiIwMDAxNjg0NjI5IiwiaHR0cDovL2xvZ2luLnNjaGVtYXMuZWJwLmNvbS9pZGVudGl0eS9jbGFpbXMvQ29udGFjdElkIjoiNTU5MTI0NyIsInNjb3BlIjpbIm9wZW5pZCIsInByb2ZpbGUiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.Nib5o0-7N19QyffazP5eGFY1A1p_uhwCkkF3Lofqambedih3GWU066JvteUMYCVRG6xBq2GZuBzu_z8GVzmNBft1204xvRQ1yZyz-LeJLZGxE0gKhRQx6aGxzNQd0HsPRgSghrf4HSceGi77vO8ZMQK_8hKMYAdYc0JMT7SpK6Ao_YoiUEGMRzrFQgipjR4OTQQazuDWCHh1ereyjdlDrzOX0Avk7SxaLYC10OAMrVtx2eO5hXEflOMckFdQbLcg8LyhMxlRWew3YAnkfoYjmONJ9fm70gGtF5ExcTeT6uoUi6D3cz7pPjaDaAuLU82JMqFR_bKtt_RuFIwNnSnK2g'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

    def get_paid_documents(self):
        """
        Fonction qui permet de récupérer les documents payés de l'API EBP.
        """
        url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders/" + self.folder_id + "/Documents/PurchaseDocument?Duration=30&DocumentType=null&ToDate=1999-01-01&Columns=DocumentNumber, Reference, CommitmentsBalanceDue&WhereCondition=%20%20type%3A%20CustomFilter%0A%20%20column%3A%20CommitmentsBalanceDue%0A%20%20operator%3A%20Equal%0A%20%20valueType%20%3A%20Decimal%0A%20%20value%3A%0A%20%20-%200"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request('GET', url, headers=headers)

        return response.text
