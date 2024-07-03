"""
Ce fichier contient les tests unitaires pour faire des tests d'insertion dans la base de données.
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
    #     return True

    def test_ajout_manuel(self):
        """
        Test d'ajout manuel des informations dans la base de données.
        """

        # ajout des logiciels EBP et Zeendoc
        database.add_logiciel("EBP")
        database.add_logiciel("Zeendoc")
        database.add_logiciel("Sellsy")

        # ajout des champs requis pour les logiciels EBP, Zeendoc et Sellsy
        database.add_champ_to_logiciel("EBP_Client_ID", "Credentials", "visible", "EBP")
        database.add_champ_to_logiciel("EBP_Client_Secret", "Credentials", "masqué", "EBP")
        database.add_champ_to_logiciel("EBP_Subscription_Key", "Credentials", "masqué", "EBP")
        database.add_champ_to_logiciel("EBP_token", "Credentials", "caché", "EBP")

        database.add_champ_to_logiciel("Zeendoc_Login", "Credentials", "visible", "Zeendoc")
        database.add_champ_to_logiciel("Zeendoc_URL_Client", "Credentials", "visible", "Zeendoc")
        database.add_champ_to_logiciel("Zeendoc_CPassword", "Credentials", "masqué", "Zeendoc")
        database.add_champ_to_logiciel("Zeendoc_CLASSEUR", "Credentials", "select_zeendoc_classeur", "Zeendoc")

        database.add_champ_to_logiciel("Sellsy_Client_ID", "Credentials", "visible", "Sellsy")
        database.add_champ_to_logiciel("Sellsy_Client_Secret", "Credentials", "masqué", "Sellsy")
        database.add_champ_to_logiciel("Sellsy_Redirect_URI", "Credentials", "visible", "Sellsy")
        database.add_champ_to_logiciel("Sellsy_token", "Credentials", "caché", "Sellsy")





        # ajout des passerelles
        database.add_passerelle("remontée de paiement")

        # connexion des logiciels aux passerelles
        id_logiciel_source = database.get_id_logiciel_by_lib_logiciel("EBP")
        database.add_passerelle_logiciel(id_passerelle=1, id_logiciel=id_logiciel_source)

        id_logiciel_destination = database.get_id_logiciel_by_lib_logiciel("Zeendoc")
        database.add_passerelle_logiciel(id_passerelle=1, id_logiciel=id_logiciel_destination)

        # ajout des champs requis pour les passerelles
        database.add_champ_to_passerelle("EBP_FOLDER_ID", "Credentials", "select_ebp_folder", "remontée de paiement")
        database.add_champ_to_passerelle("INDEX_STATUT_PAIEMENT", "Credentials", "select_zeendoc_index", "remontée de paiement")
        database.add_champ_to_passerelle("INDEX_NUM_PIECE", "Credentials", "select_zeendoc_index", "remontée de paiement")

        # # ajout du client
        # database.add_client("client1")
        # id_client = database.get_id_client_by_lib_client("client1")
        # id_passerelle = database.get_id_passerelle_by_lib_passerelle("remontée de paiement")
        # id_passerelle_client = database.add_passerelle_client(id_passerelle, id_client)

        # # ajout des champs du client
        # id_champ = database.get_id_champ_by_lib_champ("EBP_Client_ID")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="jupiterwithoutpkce")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_Client_Secret")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="78f68eac-c4e2-4221-9836-d66db48a75f0")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_Subscription_Key")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="9b90dc6db6554429a027cb43fe12ab4e")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_Login")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="marius.hivelin@gmail.com")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_URL_Client")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="deltic_demo")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CPassword")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="X?BSh:R92EmyDKi")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_FOLDER_ID")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="306851")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CLASSEUR")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="coll_21")

        # id_champ = database.get_id_champ_by_lib_champ("INDEX_STATUT_PAIEMENT")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="custom_n8")

        # id_champ = database.get_id_champ_by_lib_champ("INDEX_NUM_PIECE")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="custom_t4")

        # ajout de passerelle
        database.add_passerelle("remontée de fournisseur")

        # connexion des logiciels aux passerelles
        id_logiciel_source = database.get_id_logiciel_by_lib_logiciel("EBP")
        database.add_passerelle_logiciel(id_passerelle=2, id_logiciel=id_logiciel_source)

        id_logiciel_destination = database.get_id_logiciel_by_lib_logiciel("Zeendoc")
        database.add_passerelle_logiciel(id_passerelle=2, id_logiciel=id_logiciel_destination)

        # ajout des champs requis pour les passerelles
        database.add_champ_to_passerelle("INDEX_FOURNISSEUR", "Credentials", "select_zeendoc_index", "remontée de fournisseur")

        # # ajout du client
        # database.add_client("client2")
        # id_client = database.get_id_client_by_lib_client("client2")
        # id_passerelle = database.get_id_passerelle_by_lib_passerelle("remontée de fournisseur")
        # id_passerelle_client = database.add_passerelle_client(id_passerelle, id_client)

        # # ajout des champs du client
        # id_champ = database.get_id_champ_by_lib_champ("EBP_Client_ID")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="jupiterwithoutpkce")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_Client_Secret")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="78f68eac-c4e2-4221-9836-d66db48a75f0")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_Subscription_Key")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="9b90dc6db6554429a027cb43fe12ab4e")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_Login")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="marius.hivelin@gmail.com")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_URL_Client")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="deltic_demo")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CPassword")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="X?BSh:R92EmyDKi")

        # id_champ = database.get_id_champ_by_lib_champ("EBP_FOLDER_ID")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="306851")

        # id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CLASSEUR")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="coll_21")

        # id_champ = database.get_id_champ_by_lib_champ("INDEX_FOURNISSEUR")
        # database.add_champ_passerelle(id_passerelle_client=id_passerelle_client, id_champ=id_champ, valeur="custom_n4")

