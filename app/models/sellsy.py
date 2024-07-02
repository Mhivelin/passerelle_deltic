import json
import datetime
import urllib.parse
import requests
import base64
import hashlib
import os
from flask import Flask, request, redirect, jsonify, url_for

app = Flask(__name__)

class Sellsy:
    def __init__(self, client_id, client_secret, redirect_uri) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = None
        self.code_verifier = self.generate_code_verifier()
        self.code_challenge = self.generate_code_challenge(self.code_verifier)

    def generate_code_verifier(self):
        return base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode('utf-8')

    def generate_code_challenge(self, verifier):
        return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')

    def get_authorization_url(self):
        authorization_base_url = 'https://login.sellsy.com/oauth2/authorization'
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256'
        }
        url = f"{authorization_base_url}?{urllib.parse.urlencode(params)}"
        return url

    def fetch_token(self, authorization_response):
        token_url = 'https://login.sellsy.com/oauth2/access-tokens'
        code = urllib.parse.parse_qs(urllib.parse.urlparse(authorization_response).query).get('code')[0]
        body = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_verifier': self.code_verifier,
            'code': code
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, headers=headers, data=urllib.parse.urlencode(body))

        if response.status_code == 200:
            self.token = response.json()
            self.token['expires_at'] = datetime.datetime.now().timestamp() + self.token['expires_in']
            self.save_token(self.token)
        else:
            print(f"Failed to fetch token. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            print(f"Request Body: {body}")
            print(f"Request Headers: {headers}")
            response.raise_for_status()

    def save_token(self, token):
        with open('sellsy_token.json', 'w') as f:
            json.dump(token, f)

    def load_token(self):
        try:
            with open('sellsy_token.json', 'r') as f:
                self.token = json.load(f)
        except FileNotFoundError:
            return None

    def validate_token(self):
        if not self.token:
            self.load_token()
        if not self.token:
            return False

        expiration = self.token.get('expires_at')
        if not expiration:
            return False

        now = datetime.datetime.now().timestamp()
        if expiration < now:
            return False
        return True

    def refresh_token(self):
        token_url = 'https://login.sellsy.com/oauth2/access-tokens'
        body = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.token['refresh_token']
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, headers=headers, data=urllib.parse.urlencode(body))

        if response.status_code == 200:
            self.token = response.json()
            self.token['expires_at'] = datetime.datetime.now().timestamp() + self.token['expires_in']
            self.save_token(self.token)
        else:
            print(f"Failed to refresh token. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            response.raise_for_status()

    def get_access_token(self):
        if not self.validate_token():
            self.refresh_token()
        return self.token['access_token']

    def make_request(self, method, url, headers=None, params=None, data=None):
        if not self.token or not self.validate_token():
            print("Authenticating...")
            authorization_url = self.get_authorization_url()
            print(f"Go to the following URL and authorize access: {authorization_url}")
            return redirect(authorization_url)

        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if data is None:
            data = {}

        access_token = self.get_access_token()
        headers['Authorization'] = f'Bearer {access_token}'

        response = requests.request(method, url, headers=headers, params=params, data=data)
        return response

    def get_teams(self):
        url = "https://api.sellsy.com/v2/teams"
        response = self.make_request('GET', url)
        return response.json()