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

        # ajout des champs requis pour les logiciels EBP et Zeendoc
        database.add_champ_to_logiciel("EBP_Client_ID", "Credentials", "EBP")
        database.add_champ_to_logiciel("EBP_Client_Secret", "Credentials", "EBP")
        database.add_champ_to_logiciel("EBP_Subscription_Key", "Credentials", "EBP")
        database.add_champ_to_logiciel("EBP_token", "Credentials", "EBP")

        database.add_champ_to_logiciel("Zeendoc_Login", "Credentials", "Zeendoc")
        database.add_champ_to_logiciel("Zeendoc_URL_Client", "Credentials", "Zeendoc")
        database.add_champ_to_logiciel("Zeendoc_CPassword", "Credentials", "Zeendoc")

        # ajout des passerelles
        database.add_passerelle("remontée de paiement")

        # ajout des champs requis pour les passerelles
        database.add_champ_to_passerelle("EBP_FOLDER_ID", "remontée de paiement", "remontée de paiement")
        database.add_champ_to_passerelle("OUTPUT_INDEX", "remontée de paiement", "remontée de paiement")

        database.add_champ_to_passerelle("Zeendoc_CLASSEUR", "remontée de paiement", "remontée de paiement")
        database.add_champ_to_passerelle("INPUT_INDEX", "remontée de paiement", "remontée de paiement")

        # ajout du client
        database.add_client("client1")
        id_client = database.get_id_client_by_lib_client("client1")
        id_passerelle = database.get_id_passerelle_by_lib_passerelle("remontée de paiement")
        database.add_passerelle_client(id_passerelle, id_client)

        # ajout des champs du client
        id_champ = database.get_id_champ_by_lib_champ("EBP_Client_ID")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="jupiterwithoutpkce")

        id_champ = database.get_id_champ_by_lib_champ("EBP_Client_Secret")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="78f68eac-c4e2-4221-9836-d66db48a75f0")

        id_champ = database.get_id_champ_by_lib_champ("EBP_Subscription_Key")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="9b90dc6db6554429a027cb43fe12ab4e")

        id_champ = database.get_id_champ_by_lib_champ("Zeendoc_Login")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="marius.hivelin@gmail.com")

        id_champ = database.get_id_champ_by_lib_champ("Zeendoc_URL_Client")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="deltic_demo")

        id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CPassword")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="X?BSh:R92EmyDKi")

        id_champ = database.get_id_champ_by_lib_champ("EBP_FOLDER_ID")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="306851")

        id_champ = database.get_id_champ_by_lib_champ("Zeendoc_CLASSEUR")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="coll_21")

        id_champ = database.get_id_champ_by_lib_champ("OUTPUT_INDEX")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="DocumentNumber")

        id_champ = database.get_id_champ_by_lib_champ("INPUT_INDEX")
        database.add_champ_passerelle(id_passerelle_client=id_client, id_champ=id_champ, valeur="tempo")








    # def test_ajout_manuel(self):
    #     """
    #     Test d'ajout manuel des informations dans la base de données.
    #     """

    #     # ajout des logicels EBP et Zeendoc
    #     database.add_logiciel("EBP")
    #     database.add_logiciel("Zeendoc")

    #     # ajout des champs requis pour les logiciels EBP et Zeendoc
    #     database.add_champ("EBP_Client_ID", "EBP")
    #     database.add_champ("EBP_Client_Secret", "EBP")
    #     database.add_champ("EBP_Subscription_Key", "EBP")
    #     database.add_champ("EBP_token", "EBP")

    #     database.add_champ("Zeendoc_Login", "Zeendoc")
    #     database.add_champ("Zeendoc_URL_Client", "Zeendoc")
    #     database.add_champ("Zeendoc_CPassword", "Zeendoc")


    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Client_ID")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("EBP")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Client_Secret")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("EBP")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Subscription_Key")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("EBP")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_token")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("EBP")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_Login")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("Zeendoc")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_URL_Client")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("Zeendoc")
    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_CPassword")
    #     idLogiciel = database.get_id_logiciel_by_lib_logiciel("Zeendoc")

    #     database.add_requiert_logiciel(idChamp, idLogiciel)

    #     # ajout des passerelles
    #     lsource = database.get_id_logiciel_by_lib_logiciel("EBP")
    #     ldestination = database.get_id_logiciel_by_lib_logiciel("Zeendoc")
    #     database.add_passerelle_with_connectors("remontée de paiement", lsource, ldestination)

    #     # ajout des champs requis pour les passerelles
    #     database.add_champ("EBP_FOLDER_ID", "remontée de paiement")
    #     database.add_champ("Zeendoc_CLASSEUR", "remontée de paiement")

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_FOLDER_ID")
    #     idPasserelle = database.get_id_passerelle_by_lib_passerelle("remontée de paiement")
    #     print("idPasserelle")
    #     print(idPasserelle)
    #     database.add_requiert_passerelle(idChamp, idPasserelle)

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_CLASSEUR")
    #     idPasserelle = database.get_id_passerelle_by_lib_passerelle("remontée de paiement")
    #     print("idPasserelle")
    #     print(idPasserelle)
    #     database.add_requiert_passerelle(idChamp, idPasserelle)


    #     # ajout du client
    #     database.add_client("client1")
    #     database.add_client_passerelle(1, 1)

    #     # ajout des champs du client
    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Client_ID")
    #     database.add_champ_client(1, idChamp, "jupiterwithoutpkce")

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Client_Secret")
    #     database.add_champ_client(1, idChamp, "78f68eac-c4e2-4221-9836-d66db48a75f0")

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_Subscription_Key")
    #     database.add_champ_client(1, idChamp, "9b90dc6db6554429a027cb43fe12ab4e")

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_Login")
    #     database.add_champ_client(1, idChamp, "tests_webservices@zeendoc.com")

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_URL_Client")
    #     database.add_champ_client(1, idChamp, "tests_webservices")

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_CPassword")
    #     database.add_champ_client(1, idChamp, "tests01")

    #     idChamp = database.get_id_champ_by_lib_champ("EBP_FOLDER_ID")
    #     database.add_champ_client(1, idChamp, "306851")

    #     idChamp = database.get_id_champ_by_lib_champ("Zeendoc_CLASSEUR")
    #     database.add_champ_client(1, idChamp, "1")









