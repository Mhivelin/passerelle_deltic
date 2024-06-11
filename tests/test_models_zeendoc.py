"""
Ce module teste les fonctionnalités de la classe Zeendoc dans l'application.
Il contient des tests qui assurent le bon fonctionnement des interactions avec
l'API Zeendoc et la gestion des clients Zeendoc.
"""

import unittest
from app import create_app, db
from app.models.zeendoc import Zeendoc
from app.models import database


class TestModels(unittest.TestCase):
    """
    Classe de tests pour vérifier le comportement des modèles dans le module Zeendoc.
    """

    def create_app(self):
        """
        Créer une instance de l'application pour les tests.
        """
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Désactiver CSRF pour les tests
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        database.create_database()
        return app



    def setUp(self):
        """
        mettre en place le contexte de l'application avant chaque test.
        """
        super().setUp()
        self.app = self.create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.client.post('/login', data={"username": "admin", "password": "admin"})





    def tearDown(self):
        """
        Nettoyer le contexte de l'application après chaque test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()




    # def test_drop_table(self):
    #     """
    #     Test de la suppression de la table. (à ne pas exécuter si on veut conserver
    #     les données)
    #     """
    #     database.drop_all_tables()







    def test_zeendoc_login(self):
        """
        Teste la connexion à l'API Zeendoc.
        """

        instance_zeendoc = Zeendoc(1)

        co = instance_zeendoc.login()

        self.assertIn('Result":0,"Cookie_Duration":"38880s","Error_Msg":""', co)




    # def test_zeendoc_get_rights(self):
    #     """
    #     Teste la récupération des droits d'un utilisateur Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     rights = instance_zeendoc.get_rights()

    #     print("Rights: ", rights)

    #     self.assertIsNotNone(rights)


    # def test_getDoc(self):
    #     """
    #     Teste la récupération d'un document Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     doc_id = "1"

    #     doc = instance_zeendoc.searchDocDoc(doc_id)

    #     print("Doc: ", doc)

    #     self.assertIsNotNone(doc)


    # def test_zeendoc_updateDocPaiement(self):
    #     """
    #     Teste la définition d'un libellé pour un client Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     doc_id = "1"
    #     index = "custom_n7"


    #     print(instance_zeendoc.updateDocPaiement(doc_id, index) )




    # def test_zeendoc_get_classeurs(self):
    #     """
    #     Teste la récupération des classeurs d'un utilisateur Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     classeurs = instance_zeendoc.get_classeurs()

    #     print("Classeurs: ", classeurs)

    #     self.assertIsNotNone(classeurs)


    # def test_get_all_doc(self):
    #     """
    #     Teste la récupération de tous les documents d'un utilisateur Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     docs = instance_zeendoc.getAllDoc()

    #     print("Docs: ", docs)

    #     self.assertIsNotNone(docs)



    # def test_GetDocRef(self):
    #     """
    #     Teste la récupération d'un document Zeendoc.
    #     """

    #     instance_zeendoc = Zeendoc(1)

    #     numPiece = "FF00000001"

    #     doc = instance_zeendoc.get_doc_ref(numPiece)

    #     print("Doc: ", doc)

    #     self.assertIsNotNone(doc)



    def test_update_doc_paiement_by_ref(self):
        """
        Teste la définition d'un libellé pour un document Zeendoc.
        """

        instance_zeendoc = Zeendoc(1)

        numPiece = "FF00000001"
        index = "custom_n7"

        print(instance_zeendoc.update_doc_paiement_by_ref(numPiece, index))


if __name__ == "__main__":
    unittest.main()
