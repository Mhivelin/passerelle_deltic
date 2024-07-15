import datetime
import json
import urllib.parse
import requests
from flask import url_for
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session
from app.models import database as db


class EBP:
    """
    Classe qui permet de gérer les interactions avec l'API EBP.
    """

    def __init__(self, id) -> None:
        """Constructeur de la classe EBP."""

        self.database_Id = id
        infos = db.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(id)

        self.DateDerSynchronisation = db.get_date_synchronisation_passerelle_client(id)

        for info in infos:
            if info["LibChamp"] == "EBP_Client_ID":
                self.client_id = info["Valeur"]
            elif info["LibChamp"] == "EBP_Client_Secret":
                self.client_secret = info["Valeur"]
            elif info["LibChamp"] == "EBP_Subscription_Key":
                self.ebp_subscription_key = info["Valeur"]
            elif info["LibChamp"] == "EBP_FOLDER_ID":
                self.folder_id = info["Valeur"]
            elif info["LibChamp"] == "EBP_token":
                self.token = json.loads(info["Valeur"])
                self.refresh_token_value = self.token["refresh_token"]

    def validate_token(self, token):
        """Valide si le token est encore valide."""
        valeur = token.get("Valeur")
        if not valeur:
            return False

        valeur_dict = json.loads(valeur)
        expiration = valeur_dict.get("expires_at")
        if expiration is None:
            return False

        now = datetime.datetime.now().timestamp()
        if expiration < now:
            return False
        return True

    def is_authenticated(self):
        """
        Vérifie si l'utilisateur est déjà authentifié.
        """
        token = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(
            self.database_Id, "EBP_token"
        )
        if token and self.validate_token(token):
            return True
        return False

    def refresh_token(self):
        """
        Rafraîchit le token d'accès
        """
        url = "https://api-login.ebp.com/connect/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token_value,
        }

        try:
            response = requests.post(
                url, headers=headers, data=urllib.parse.urlencode(body)  # Utilisation de data= pour URL-encoding
            )

            if response.status_code == 200:
                new_token = response.json()
                self.Bdtoken_saver(new_token)
                return new_token
            else:
                print(f"Échec du rafraîchissement du token. Code d'état: {response.status_code}")
                print(f"Texte de la réponse: {response.text}")
                print(f"Corps de la requête: {body}")
                print(f"En-têtes de la requête: {headers}")
                response.raise_for_status()

        except HTTPError as http_err:
            print(f"Erreur HTTP: {http_err}")
        except Exception as err:
            print(f"Autre erreur: {err}")

    def login(self):
        """
        Gère le processus de connexion à l'API EBP.
        """
        authorization_base_url = "https://api-login.ebp.com/connect/authorize"
        token_url = "https://api-login.ebp.com/connect/token"
        redirect_uri = url_for(
            "ebp.SignInRedirect", IdPasserelleClient=self.client_id, _external=True
        )
        scope = ["openid", "profile", "offline_access"]

        token = None

        try:
            token = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(
                self.database_Id, "EBP_token"
            )
        except Exception as e:
            print("Erreur lors de la récupération du token de la base de données:", e)

        if not token:
            oauth = OAuth2Session(
                self.client_id, redirect_uri=redirect_uri, scope=scope
            )
            authorization_url, state = oauth.authorization_url(authorization_base_url)
            print("Aller à %s et autoriser l'accès." % authorization_url)
            authorization_response = input("Entrez l'URL de redirection: ")
            token = oauth.fetch_token(
                token_url,
                authorization_response=authorization_response,
                client_secret=self.client_secret,
            )
            if token:
                self.Bdtoken_saver(token)
        elif not self.validate_token(token):
            print("Le token est invalide, rafraîchissement...")
            token = self.refresh_token()

        self.token = token
        return token

    def callback(self, code, IdClient):  # pylint: disable=C0103
        """
        Fonction de rappel pour gérer le code d'autorisation
        """
        redirect_uri = url_for(
            "ebp.SignInRedirect", IdPasserelleClient=IdClient, _external=True
        )
        token_url = "https://api-login.ebp.com/connect/token"

        try:
            oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri)
            token = oauth.fetch_token(
                token_url, client_secret=self.client_secret, code=code
            )
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
        """
        Crée une session OAuth2 avec le token fourni.
        """
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

    def Bdtoken_saver(self, token):  # pylint: disable=C0103
        """
        Enregistre le token dans la base de données.
        """
        print("Début de l'enregistrement du token")
        token_json = json.dumps(token)

        # on vérifie si le token existe déjà
        token_db = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(
            self.database_Id, "EBP_token"
        )
        print("Token de la base de données:", token_db)
        if token_db:
            try:
                id_champ = db.get_id_champ_by_lib_champ("EBP_token")
                db.update_champ_passerelle(self.database_Id, id_champ, token_json)
                print("Token mis à jour avec succès.")
            except Exception as e:
                print("Erreur lors de la mise à jour du token:", e)

        else:
            try:
                id_champ = db.get_id_champ_by_lib_champ("EBP_token")
                db.add_champ_passerelle(self.database_Id, id_champ, token_json)
                print("Token enregistré avec succès.")
            except Exception as e:
                print("Erreur lors de l'enregistrement du token:", e)

    def make_request(
        self, method, url, headers=None, params=None, data=None
    ):  # pylint: disable=R0913
        """
        Effectue une requête HTTP à l'API EBP.
        """
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
            headers["Authorization"] = f"Bearer {access_token}"
        else:
            raise ValueError("Access token is missing or expired")

        response = requests.request(
            method, url, headers=headers, params=params, data=data, timeout=10
        )
        return response

    def get_folders(self):
        """
        Récupère les dossiers EBP.
        """
        url = "https://api-developpeurs.ebp.com/gescom/api/v1/Folders?Offset=0&Limit=100&Accept-Language=fr-FR"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request("GET", url, headers=headers)
        res = response.text
        res = json.loads(res)
        res = res["folders"]
        return res

    def get_suppliers(self):
        """
        Récupère les fournisseurs.
        """
        url = f"https://api-developpeurs.ebp.com/gescom/api/v1/Folders/{self.folder_id}/GenericQuery?TableName=supplier&Columns=name, Id, Accounts_Account&=2020-11-06"
        headers = {"ebp-subscription-key": self.ebp_subscription_key}
        response = self.make_request("GET", url, headers=headers)
        return response.text

    def get_paid_documents(self):
        """
        Récupère les documents payés.
        """
        date_recherche = self.DateDerSynchronisation
        date_recherche = datetime.datetime.strptime(date_recherche, "%Y-%m-%d")
        date_recherche = date_recherche - datetime.timedelta(days=2)

        date_premier_doc = "1990-01-01"
        date_premier_doc = datetime.datetime.strptime(date_premier_doc, "%Y-%m-%d")

        date_recherche_str = date_recherche.strftime("%Y-%m-%dT%H:%M:%S")

        url = (f"https://api-developpeurs.ebp.com/gescom/api/v1/Folders/{self.folder_id}/Documents/"
            f"PurchaseDocument?Duration=30&DocumentType=null&ToDate={date_premier_doc}"
            f"&Columns=DocumentNumber,Reference,CommitmentsBalanceDue,sysModifiedDate"
            f"&SysModifiedDate={date_recherche_str}"
            f"&WhereCondition=%20%20type%3A%20CustomFilter%0A%20%20column%3A%20CommitmentsBalanceDue%0A"
            f"%20%20operator%3A%20Equal%0A%20%20valueType%20%3A%20Decimal%0A%20%20value%3A%0A%20%20-%200")

        print(url)

        headers = {
            "ebp-subscription-key": self.ebp_subscription_key
        }

        response = self.make_request("GET", url, headers=headers)
        return response.text
