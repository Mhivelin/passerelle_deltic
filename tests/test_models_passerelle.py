"""
Ce fichier contient les tests unitaires pour faire les tests de l'oject passerelle.
"""

import unittest
import datetime

from app import create_app
from app.models import database, passerelles


class TestModels(unittest.TestCase):
    """
    CLasse de test pour les opérations de la base de données.
    """

    def setUp(self):
        """
        mettre en place le contexte de l'application avant chaque test.
        """
        # Créer une instance de l'application
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Créer la base de données
        database.create_database()

    def tearDown(self):
        """
        Nettoyer le contexte de l'application après chaque test.
        """
        self.app_context.pop()

    # def test_login(self):
    #     """
    #     Test de la fonction login du model zeendoc.
    #     """

    # def test_routine(self):
    #     """
    #     Test de la fonction routine.
    #     """
    #     result = passerelles.routine()

    #     print(result)

    def test_p_remonte_paiement_ebp_zeendoc(self):
        """
        Test de la fonction P_remonte_paiement.
        """

        database.reset_date_synchronisation_passerelle_client(2)

        value = datetime.datetime.now().strftime("%Y-%m-%d")
        passerelles.p_remonte_paiement_ebp_zeendoc(2, value)

    # def test_P_remonte_fournisseur(self):
    #     """
    #     Test de la fonction P_remonte_fournisseur.
    #     """
    #     passerelles.P_remonte_fournisseur(2)

    # def test_P_remonte_paiement_Sellsy_Zeendoc(self):
    #     """
    #     Test de la fonction P_remonte_paiement_Sellsy_Zeendoc.
    #     """
    #     passerelles.P_remonte_paiement_Sellsy_Zeendoc(1)
