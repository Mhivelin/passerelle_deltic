"""
Ce fichier contient les tests unitaires pour faire les tests de l'oject passerelle.
"""



import unittest
from app import create_app
from app.models import passerelles, database

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



    def test_routine(self):
        """
        Test de la fonction routine.
        """
        result = passerelles.routine()


    # def test_P_remonte_paiement(self):
    #     """
    #     Test de la fonction P_remonte_paiement.
    #     """
