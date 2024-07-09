import requests
import json
from requests.auth import HTTPBasicAuth
from app.models import database as db
import time

class Sellsy:
    def __init__(self, passerelle_client_id, scope="all"):
        infos = db.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(passerelle_client_id)

        self.token = None

        for info in infos:
            if info["LibChamp"] == "Sellsy_Client_ID":
                self.client_id = info["Valeur"]
            elif info["LibChamp"] == "Sellsy_Client_Secret":
                self.client_secret = info["Valeur"]
            elif info["LibChamp"] == "Sellsy_token":
                token_info = json.loads(info["Valeur"])
                self.token = token_info.get("access_token")
                self.token_expiry = token_info.get("expires_in") + time.time()

        self.databaseId = passerelle_client_id
        self.auth_host = "https://login.sellsy.com"
        self.api_host = "https://api.sellsy.com"
        self.scope = scope



        if not self.token or self.token_is_expired():
            print("Token non trouvé ou expiré, on en génère un nouveau.")
            self.get_token()

    def Bdtoken_saver(self, token):
        print("Début de l'enregistrement du token")
        token_json = json.dumps(token)

        # on vérifie si le token existe déjà
        token_db = db.get_champ_passerelle_by_passerelle_client_and_lib_champ(self.databaseId, "Sellsy_token")
        print("Token de la base de données:", token_db)
        if token_db:
            try:
                idChamp = db.get_id_champ_by_lib_champ("Sellsy_token")
                db.update_champ_passerelle(self.databaseId, idChamp, token_json)
                print("Token mis à jour avec succès.")
            except Exception as e:
                print("Erreur lors de la mise à jour du token:", e)
        else:
            try:
                idChamp = db.get_id_champ_by_lib_champ("Sellsy_token")
                db.add_champ_passerelle(self.databaseId, idChamp, token_json)
                print("Token enregistré avec succès.")
            except Exception as e:
                print("Erreur lors de l'enregistrement du token:", e)

    def token_is_expired(self):
        return time.time() > self.token_expiry

    def get_token(self):
        url = f"{self.auth_host}/oauth2/access-tokens"
        print(f"Getting token from URL: {url}")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        response = requests.post(url, data=data, auth=HTTPBasicAuth(self.client_id, self.client_secret))
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.status_code} - {response.text}")

        response_data = response.json()
        self.token = response_data['access_token']
        self.token_expiry = response_data['expires_in'] + time.time()
        self.Bdtoken_saver(response_data)

        return self.token

    def make_request(self, endpoint, method='GET', data=None):
        if not self.token or self.token_is_expired():
            self.get_token()

        url = f"{self.api_host}/{endpoint}"
        headers = {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=data)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, json=data)
        else:
            raise ValueError(f"HTTP method {method} is not supported")

        if response.status_code == 401:
            print("Token expiré ou invalide, régénération du token.")
            self.get_token()
            headers['Authorization'] = f"Bearer {self.token}"
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, json=data)

        if response.status_code >= 400:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response.json()

    def get_invoices(self, limit=100):
        endpoint = "v2/invoices"
        params = {
            'field[]': ['id', 'number', 'status', 'date', 'amount'],
            'order': 'date',
            'limit': limit
        }

        try:
            response = self.make_request(endpoint, method='GET', data=params)
            return response['data']
        except Exception as e:
            print(f"Erreur lors de la récupération des factures: {e}")
            return None




    def get_paid_invoices(self):
        invoices = self.get_invoices()

        if not invoices:
            return None

        paid_invoices = [invoice for invoice in invoices if invoice.get('status') == 'paid']

        return paid_invoices



    def get_invoice_payments(self, invoice_id):
        endpoint = f"v2/invoices/{invoice_id}/payments"
        try:
            response = self.make_request(endpoint, method='GET')
            return response
        except Exception as e:
            print(f"Erreur lors de la récupération des paiements pour la facture {invoice_id}: {e}")
            return None


    def get_paid_invoices_with_last_payment(self):
        paid_invoices = self.get_paid_invoices()
        if not paid_invoices:
            return None

        for invoice in paid_invoices:
            payments = self.get_invoice_payments(invoice['id'])

            # {'data': [{'id': 28098129, 'number': 'test', 'paid_at': '2024-07-03T11:00:48+02:00', 'status': 'confirmed', 'payment_method_id': 5694078, 'type': 'credit', 'amount': {'value': '64.80', 'currency': 'EUR'}, 'related': [{'type': 'invoice', 'id': 51134735}]}], 'pagination': {'limit': 25, 'count': 1, 'total': 1, 'offset': 'WyIxNzE5OTk3MjQ4Il0='}}

            if payments:
                # récuperer le paiement avec la date la plus récente
                last_payment = max(payments['data'], key=lambda x: x['paid_at'])
                invoice['last_payment'] = last_payment

        return paid_invoices








