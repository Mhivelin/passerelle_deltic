"""
Ce module contient les tests des routes liées à la base de données de l'application.
"""
# permet de désactiver les avertissements inutiles de pylint
# nombre maximum de méthodes autorisées :
# pylint: disable=R0904

from flask_testing import TestCase
from flask_login import login_user
from app import create_app, db
from app.models.user import User
from app.models import database



class TestRoutes(TestCase):
    """
    Classe de test pour les routes liées à la base de données.
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




    def login(self, username, password):
        """
        Fonction de connexion pour les tests
        """

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return True
        return False


    # def test_drop_table(self):
    #     """
    #     Test de la suppression de la table. (à ne pas exécuter si on veut conserver
    #     les données)
    #     """
    #     database.drop_all_tables()


    def test_login(self):
        """
        Teste la route login
        """
        response = self.client.post("/login", data={
            "username": "admin",
            "password": "admin"
        }, follow_redirects=True)


        self.assertEqual(response.status_code, 200)
        self.assertIn('Liste des Clients', response.data.decode())




# @database_bp.route("/database/add_passerelle_with_connectors_and_fields", methods=["POST"])
# @login_required
# def add_passerelle_with_connectors_and_fields():
#     """
#     Ajoute une passerelle à la base de données avec un connecteur source et un connecteur destination.
#     """
#     # obtenir les données de la requête (soit en JSON, soit en form-data)
#     if request.is_json:
#         data = request.get_json()
#     else:
#         data = request.form

#     print("data: ", data)


#     # ajouter la passerelle
#     database.add_passerelle_with_connectors(
#         data["lib_passerelle"],
#         data["id_logiciel_source"],
#         data["id_logiciel_destination"])

#     # ajouter les champs
#     for champ in data["requis"]:
#         print("champ: ", champ)
#         database.add_requiere_passerelle(champ, data["id_passerelle"])

#     return redirect(url_for("v_interface.home"))



    def test_add_passerelle_with_connectors_and_fields(self):
        """
        Teste la route add_passerelle_with_connectors_and_fields
        """
        # Simuler une connexion
        self.login("admin", "admin")

        response = self.client.post("/database/add_passerelle_with_connectors_and_fields", data={
            "lib_passerelle": "passerelle_test",
            "id_logiciel_source": 1,
            "id_logiciel_destination": 2,
            "requis": ["champ1", "champ2"]
        }, follow_redirects=True)



        self.assertEqual(response.status_code, 200)
        self.assertIn('{"status":"success"}', response.data.decode())

        # supprimer les données ajoutées
        id_passerelle = database.get_id_passerelle_by_lib_passerelle("passerelle_test")

        print("id_passerelle: ", id_passerelle)
        print("logiciel pass: ", database.get_logiciel_by_passerelle(id_passerelle))

        database.delete_passerelle(id_passerelle)
