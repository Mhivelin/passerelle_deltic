import unittest
from app import create_app
from app.models.sellsy import Sellsy
import os
from app.models import database


class TestModels(unittest.TestCase):
    """
    Classe de cas de test pour vérifier le bon fonctionnement des modèles relatifs à EBP.
    """

    def setUp(self):
        """
        Initialise l'application et le contexte avant chaque test.
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Nettoie le contexte après chaque test.
        """
        self.app_context.pop()

    def test_init(self):
        """
        Teste l'initialisation de l'objet Sellsy.
        """
        client_id = "580e4e47-2095-49ab-b0a5-afb7f0419901"
        client_secret = "cfb45ad9d142eb0ea13ff24d8b7b1e53f4d5a7698abeec1ff4b0ae19846c4473"
        redirect_uri = "http://localhost:5000/sellsy/callback"

        sellsy = Sellsy(client_id, client_secret, redirect_uri)

        redirect_url = sellsy.get_authorization_url()

        print(redirect_url)





