"""
Ce fichier contient les tests unitaires pour les opérations de la base de données.
les premier test est ont des commentaire pour expliquer le principe de fonctionnement
mais les autres non.

"""




import unittest
from app import create_app
from app.models import database


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


    # def test_drop_table(self):
    #     """
    #     Test de la suppression de la table. (à ne pas exécuter si on veut conserver
    #     les données)
    #     """
    #     database.drop_all_tables()

    #     database.drop_table("LOGICIEL_CLIENT")
    #     database.drop_table("LOGICIEL_CLIENT_EBP")
    #     database.drop_table("LOGICIEL_CLIENT_ZEENDOC")



    def test_create_database(self):
        """
        Test de la création de la base de données.
        """
        # deja fait dans le setUp mais on le refait pour le test
        database.create_database()
        self.assertIsNotNone(database.get_all_passerelles())

    def test_passerelle_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de passerelle.
        """

        # ajout d'une passerelle
        database.add_passerelle("passerelle1")

        # récupération de la passerelle
        passerelle = database.get_passerelle_by_id(1)

        # vérification de l'existence de la passerelle
        self.assertIsNotNone(passerelle)

        # suppression de la passerelle
        database.delete_passerelle(1)

        # vérification de la suppression de la passerelle
        self.assertIsNone(database.get_passerelle_by_id(1))


    def test_logiciel_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de logiciel.
        """
        database.add_logiciel("logiciel1")
        logiciel = database.get_logiciel_by_id(1)
        self.assertIsNotNone(logiciel)
        database.delete_logiciel(1)
        self.assertIsNone(database.get_logiciel_by_id(1))


    def test_client_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de client.
        """
        database.add_client("client1")
        client = database.get_client_by_id(1)
        self.assertIsNotNone(client)
        database.delete_client(1)
        self.assertIsNone(database.get_client_by_id(1))


    def test_connecteur_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de connecteur
        (source et destination)
        """
        # ajout d'un logiciel et d'une passerelle pour tester les connecteurs
        database.add_logiciel("logiciel1")
        database.add_passerelle("passerelle1")

        database.add_connecteur_source(1, 1)
        connecteur_source = database.get_connecteur_source_by_id(1)
        self.assertIsNotNone(connecteur_source)
        database.delete_connecteur_source(1)
        self.assertIsNone(database.get_connecteur_source_by_id(1))

        database.add_connecteur_destination(1, 1)
        connecteur_destination = database.get_connecteur_destination_by_id(1)
        self.assertIsNotNone(connecteur_destination)
        database.delete_connecteur_destination(1)
        self.assertIsNone(database.get_connecteur_destination_by_id(1))

        database.delete_logiciel(1)
        database.delete_passerelle(1)



    def test_client_passerelle_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de client passerelle.
        """
        database.add_client("client1")
        database.add_passerelle("passerelle1")
        database.add_client_passerelle(1, 1)
        client_passerelle = database.get_client_passerelle_by_id(1, 1)
        self.assertIsNotNone(client_passerelle)
        database.delete_client_passerelle(1, 1)
        self.assertIsNone(database.get_client_passerelle_by_id(1, 1))
        database.delete_client(1)
        database.delete_passerelle(1)



    def test_requiere_operations(self):
        """
        Test d'ajout, de récupération et de suppression des enregistrements de requiere.
        """
        database.add_champ("requis1", "table1")
        self.assertIsNotNone(database.get_all_champs())

        database.add_requiere_logiciel(1, 1)
        self.assertIsNotNone(database.get_all_requiere())


        database.delete_requiere_logiciel(1, 1)
        database.delete_champ(1)



