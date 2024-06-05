import pytest
from flask import Flask, url_for
from flask_login import LoginManager, login_user, UserMixin
from app.models import database, user

@pytest.fixture
def app():
    """
    Fixture pour configurer l'application Flask pour les tests.
    """
    app = Flask(__name__)
    app.register_blueprint(database_bp)
    app.register_blueprint(v_user_bp)  # Assurez-vous que le blueprint d'authentification est enregistré
    app.config['TESTING'] = True
    app.config['LOGIN_DISABLED'] = False
    app.secret_key = 'supersecretkey'  # Nécessaire pour les sessions

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))

    return app

@pytest.fixture
def client(app):
    """
    Fixture pour configurer un client de test.
    """
    return app.test_client()

@pytest.fixture(scope='function')
def db_setup():
    """
    Fixture pour la configuration de la base de données.
    """
    database.create_database()
    # Ajout d'un utilisateur de test
    user = user(username="test", password="")
    user.set_password("test")
    database.db.session.add(user)
    database.db.session.commit()
    yield
    database.drop_all_tables()

class TestRoutes:

    def login(self, client, username, password):
        """
        Fonction de connexion pour les tests
        """
        return client.post('/login', data={"username": username, "password": password}, follow_redirects=True)

    def test_login(self, client, db_setup):
        """
        Test de la route de connexion.
        """
        response = self.login(client, "test", "test")
        assert response.status_code == 200
        assert 'Invalid username or password' not in response.data.decode()

    def test_get_all_clients(self, client, db_setup):
        """
        Test de la route pour obtenir tous les clients.
        """
        response = client.get('/database/client')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_add_client(self, client, db_setup):
        """
        Test de la route pour ajouter un client.
        """
        response = client.post('/database/client', json={"username": "test_user"})
        assert response.status_code == 201
        assert response.json['message'] == "Client added successfully"

        # Vérifie que le client a été ajouté
        response = client.get('/database/client')
        clients = response.json
        assert len(clients) == 1
        assert clients[0]['Username'] == "test_user"

    def test_delete_client(self, client, db_setup):
        """
        Test de la route pour supprimer un client.
        """
        # Ajoute un client pour le test
        client.post('/database/client', json={"username": "test_user"})

        # Récupère l'ID du client ajouté
        response = client.get('/database/client')
        id_client = response.json[0]['IdClient']

        # Supprime le client
        response = client.delete(f'/database/client/{id_client}')
        assert response.status_code == 200
        assert response.json['message'] == "Client deleted successfully"

        # Vérifie que le client a été supprimé
        response = client.get('/database/client')
        assert len(response.json) == 0

    def test_get_all_passerelles(self, client, db_setup):
        """
        Test de la route pour obtenir toutes les passerelles.
        """
        response = client.get('/database/passerelle')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_add_passerelle(self, client, db_setup):
        """
        Test de la route pour ajouter une passerelle.
        """
        response = client.post('/database/passerelle', json={"LibPasserelle": "test_passerelle"})
        assert response.status_code == 201
        assert response.json['message'] == "Passerelle added successfully"

        # Vérifie que la passerelle a été ajoutée
        response = client.get('/database/passerelle')
        passerelles = response.json
        assert len(passerelles) == 1
        assert passerelles[0]['LibPasserelle'] == "test_passerelle"

    def test_delete_passerelle(self, client, db_setup):
        """
        Test de la route pour supprimer une passerelle.
        """
        # Ajoute une passerelle pour le test
        client.post('/database/passerelle', json={"LibPasserelle": "test_passerelle"})

        # Récupère l'ID de la passerelle ajoutée
        response = client.get('/database/passerelle')
        id_passerelle = response.json[0]['IdPasserelle']

        # Supprime la passerelle
        response = client.delete(f'/database/passerelle/{id_passerelle}')
        assert response.status_code == 200
        assert response.json['message'] == "Passerelle deleted successfully"

        # Vérifie que la passerelle a été supprimée
        response = client.get('/database/passerelle')
        assert len(response.json) == 0

    # Ajoutez des tests similaires pour les autres routes

    def test_get_all_logiciels(self, client, db_setup):
        """
        Test de la route pour obtenir tous les logiciels.
        """
        response = client.get('/database/logiciel')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_add_logiciel(self, client, db_setup):
        """
        Test de la route pour ajouter un logiciel.
        """
        response = client.post('/database/logiciel', json={"lib_logiciel": "test_logiciel"})
        assert response.status_code == 201
        assert response.json['message'] == "Logiciel added successfully"

        # Vérifie que le logiciel a été ajouté
        response = client.get('/database/logiciel')
        logiciels = response.json
        assert len(logiciels) == 1
        assert logiciels[0]['LibLogiciel'] == "test_logiciel"

    def test_delete_logiciel(self, client, db_setup):
        """
        Test de la route pour supprimer un logiciel.
        """
        # Ajoute un logiciel pour le test
        client.post('/database/logiciel', json={"lib_logiciel": "test_logiciel"})

        # Récupère l'ID du logiciel ajouté
        response = client.get('/database/logiciel')
        id_logiciel = response.json[0]['IdLogiciel']

        # Supprime le logiciel
        response = client.delete(f'/database/logiciel/{id_logiciel}')
        assert response.status_code == 200
        assert response.json['message'] == "Logiciel deleted successfully"

        # Vérifie que le logiciel a été supprimé
        response = client.get('/database/logiciel')
        assert len(response.json) == 0

    def test_get_all_champs(self, client, db_setup):
        """
        Test de la route pour obtenir tous les champs.
        """
        response = client.get('/database/champ')
        assert response.status_code == 200
        assert isinstance(response.json, list)

    def test_add_champ(self, client, db_setup):
        """
        Test de la route pour ajouter un champ.
        """
        response = client.post('/database/champ', json={"lib_champ": "test_champ", "nom_table": "test_table"})
        assert response.status_code == 201
        assert response.json['message'] == "Champ added successfully"

        # Vérifie que le champ a été ajouté
        response = client.get('/database/champ')
        champs = response.json
        assert len(champs) == 1
        assert champs[0]['LibChamp'] == "test_champ"

    def test_delete_champ(self, client, db_setup):
        """
        Test de la route pour supprimer un champ.
        """
        # Ajoute un champ pour le test
        client.post('/database/champ', json={"lib_champ": "test_champ", "nom_table": "test_table"})

        # Récupère l'ID du champ ajouté
        response = client.get('/database/champ')
        id_champ = response.json[0]['IdChamp']

        # Supprime le champ
        response = client.delete(f'/database/champ/{id_champ}')
        assert response.status_code == 200
        assert response.json['message'] == "Champ deleted successfully"

        # Vérifie que le champ a été supprimé
        response = client.get('/database/champ')
        assert len(response.json) == 0

    def test_add_passerelle_with_connectors_and_fields(self, client, db_setup):
        """
        Test pour ajouter une passerelle avec des connecteurs et des champs.
        """
        # Connectez-vous en tant qu'test
        response = self.login(client, "test", "test")
        assert response.status_code == 200

        response = client.post('/database/add_passerelle_with_champs', data={
            "LibPasserelle": "test_passerelle",
            "id_logiciel_source": 1,
            "id_logiciel_destination": 2,
            "requis[]": [1, 2]
        })
        assert response.status_code == 201
        assert response.json['message'] == "Passerelle added successfully"

        # Vérifie que la passerelle et les champs ont été ajoutés
        response = client.get('/database/passerelle')
        passerelles = response.json
        assert len(passerelles) == 1
        assert passerelles[0]['LibPasserelle'] == "test_passerelle"
