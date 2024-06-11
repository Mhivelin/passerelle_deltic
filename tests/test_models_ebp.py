import unittest
from app import create_app
from app.models.ebp import EBP
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




    def test_login(self):
        """
        Teste la connexion à l'API EBP.
        """

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


        ebp = EBP(1)
        ebp.login()

        print("Token: ", ebp.token)

        if not ebp.is_authenticated():
            ebp.refresh_token()



        # suppression du token pour les prochains tests
        # database.delete_champ_client_libelle("EBP_token", 1)

    # def test_refresh_token(self):
    #     """
    #     Teste le rafraîchissement du token EBP.
    #     """

    #     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    #     ebp = EBP(1)
    #     ebp.refresh_token()

    #     print("Token: ", ebp.token)




    def test_get_folders(self):
        """
        Teste la récupération des dossiers EBP.
        """

        # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        ebp = EBP(1)
        folders = ebp.get_folders()
        print("Folders: ", folders)


    # def test_get_suppliers(self):
    #     """
    #     Teste la récupération des fournisseurs EBP.
    #     """

    #     os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    #     ebp = EBP(1)
    #     suppliers = ebp.get_suppliers()
    #     print("Suppliers: ", suppliers)

    def test_get_paid_documents(self):
        """
        Teste la récupération des documents payés EBP.
        """

        # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        ebp = EBP(1)
        paid_documents = ebp.get_paid_documents()
        print("Paid documents: ", paid_documents)




if __name__ == "__main__":
    unittest.main()

