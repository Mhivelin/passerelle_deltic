"""
Ce fichier contient des tests temporaires pour les opérations de la base de données.
"""



import unittest
from app import create_app
from app.models import database, zeendoc

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


    # def test_get_champs_by_logiciels(self):
    #     """
    #     Test de la fonction get_champs_by_logiciels
    #     """
    #     logiciels = "1"
    #     champs = database.get_champs_by_logiciels(logiciels)

    #     print(champs)


    # def test_get_champ_by_client_with_lib_champ(self):
    #     """
    #     Test de la fonction get_champ_by_client_with_lib_champ
    #     """
    #     id_client = 1  # ID du client à tester
    #     champs = database.get_all_champs_for_client(id_client)
    #     for champ in champs:
    #         print(champ)

    # def test_get_passerelles_by_client(self):
    #     """
    #     Test de la fonction get_passerelles_by_client
    #     """
    #     id_client = 1
    #     passerelles = database.get_passerelles_by_client(id_client)
    #     for passerelle in passerelles:
    #         print(passerelle)


    # def test_get_logiciels_by_passerelles(self):
    #     """
    #     Test de la fonction get_logiciels_by_passerelles
    #     """
    #     id_passerelle = "1"
    #     logiciels = database.get_logiciels_by_passerelles(id_passerelle)
    #     for logiciel in logiciels:
    #         print(logiciel)


    # def test_add_multiple_champ_passerelle(self):
    #     """
    #     Test de la fonction add_multiple_champ_passerelle
    #     """
    #     id_passerelle = 1
    #     champs = [
    #         {
    #             "id_champ": 1,
    #             "Valeur": "Valeur1"
    #         },
    #         {
    #             "id_champ": 2,
    #             "Valeur": "machin"
    #         },
    #         {
    #             "id_champ": 3,
    #             "Valeur": "Valeur3"
    #         }
    #     ]
    #     database.add_or_update_champ_passerelle(id_passerelle, champs)



    # def test_get_champ_passerelle_client_by_client_with_lib_champ(self):
    #     """
    #     Test de la fonction get_champ_passerelle_client_by_client_with_lib_champ
    #     """
    #     id_client = 1
    #     champs = database.get_champ_passerelle_client_by_client_with_lib_champ(id_client)
    #     for champ in champs:
    #         print(champ)

    # def test_get_all_champs_for_client(self):
    #     """
    #     Test de la fonction get_all_champs_for_client
    #     """
    #     id_client = 1
    #     champs = database.get_all_champs_for_client(id_client)
    #     for champ in champs:
    #         print(champ)


    def test_zeendoc_get_index(self):
        """
        Test de la fonction get_index de la classe Zeendoc
        """
        id_client = 1
        instance_zeendoc = zeendoc.Zeendoc(id_client)
        instance_zeendoc.get_rights()
        index = instance_zeendoc.get_index()
        print("liste des index: ", index)
