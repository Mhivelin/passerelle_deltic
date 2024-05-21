import pytest
from app.models import database

@pytest.fixture(scope='function')
def db_connection():
    """
    Fixture pour la connexion à la base de données.
    Configure la base de données avant chaque test et la nettoie après chaque test.
    """
    # Setup: Création de la base de données et des tables
    database.create_database()
    conn = database.get_db_connexion()
    yield conn
    # Teardown: Suppression des tables après chaque test
    database.drop_all_tables()
    conn.close()

def test_create_database(db_connection):
    """
    Test de création de la base de données.
    Vérifie que toutes les tables nécessaires sont créées.
    """
    conn = db_connection
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table['name'] for table in cursor.fetchall()]
    assert "CLIENT" in tables
    assert "LOGICIEL" in tables
    assert "PASSERELLE" in tables
    assert "CHAMPS" in tables
    assert "CHAMP_PASSERELLE" in tables
    assert "CONNECT_LOGICIEL" in tables
    assert "PASSERELLE_CLIENT" in tables

def test_add_client(db_connection):
    """
    Test d'ajout d'un client.
    Vérifie que le client est correctement ajouté à la base de données.
    """
    database.add_client("test_user")
    clients = database.get_all_clients()
    assert len(clients) == 1
    assert clients[0]['Username'] == "test_user"

def test_add_and_get_passerelle(db_connection):
    """
    Test d'ajout d'une passerelle et de récupération par identifiant.
    Vérifie que la passerelle est correctement ajoutée et récupérée.
    """
    database.add_passerelle("test_passerelle")
    passerelles = database.get_all_passerelles()
    assert len(passerelles) == 1
    assert passerelles[0]['LibPasserelle'] == "test_passerelle"
    passerelle = database.get_passerelle_by_id(passerelles[0]['IdPasserelle'])
    assert passerelle['LibPasserelle'] == "test_passerelle"

def test_add_and_get_logiciel(db_connection):
    """
    Test d'ajout d'un logiciel et de récupération par identifiant.
    Vérifie que le logiciel est correctement ajouté et récupéré.
    """
    database.add_logiciel("test_logiciel")
    logiciels = database.get_all_logiciels()
    assert len(logiciels) == 1
    assert logiciels[0]['LibLogiciel'] == "test_logiciel"
    logiciel = database.get_logiciel_by_id(logiciels[0]['IdLogiciel'])
    assert logiciel['LibLogiciel'] == "test_logiciel"

def test_add_and_get_champ(db_connection):
    """
    Test d'ajout d'un champ et de récupération par identifiant.
    Vérifie que le champ est correctement ajouté et récupéré.
    """
    database.add_champ("test_champ", "test_table")
    champs = database.get_all_champs()
    assert len(champs) == 1
    assert champs[0]['LibChamp'] == "test_champ"
    champ = database.get_champ_by_id(champs[0]['IdChamp'])
    assert champ['LibChamp'] == "test_champ"

def test_add_and_get_connecteur(db_connection):
    """
    Test d'ajout d'un connecteur et de récupération par identifiant.
    Vérifie que le connecteur est correctement ajouté et récupéré.
    """
    database.add_logiciel("test_logiciel")
    database.add_passerelle("test_passerelle")
    id_logiciel = database.get_id_logiciel_by_lib_logiciel("test_logiciel")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_connecteur(id_logiciel, id_passerelle, True)
    connecteurs = database.get_all_connecteurs()
    assert len(connecteurs) == 1
    assert connecteurs[0]['IdLogiciel'] == id_logiciel
    assert connecteurs[0]['IdPasserelle'] == id_passerelle

def test_add_and_get_champ_passerelle(db_connection):
    """
    Test d'ajout d'un champ passerelle et de récupération par identifiant.
    Vérifie que le champ passerelle est correctement ajouté et récupéré.
    """
    database.add_client("test_user")
    database.add_passerelle("test_passerelle")
    id_client = database.get_id_client_by_lib_client("test_user")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_passerelle_client(id_passerelle, id_client)
    passerelle_clients = database.get_all_passerelle_client()
    id_passerelle_client = passerelle_clients[0]['IdPasserelleClient']
    database.add_champ("test_champ", "test_table")
    id_champ = database.get_id_champ_by_lib_champ("test_champ")
    database.add_champ_passerelle(id_passerelle_client, id_champ, "test_value")
    champ_passerelles = database.get_all_champ_passerelle()
    assert len(champ_passerelles) == 1
    assert champ_passerelles[0]['Valeur'] == "test_value"

def test_delete_client(db_connection):
    """
    Test de suppression d'un client.
    Vérifie que le client est correctement supprimé de la base de données.
    """
    database.add_client("test_user")
    clients = database.get_all_clients()
    assert len(clients) == 1
    id_client = clients[0]['IdClient']
    database.delete_client(id_client)
    clients = database.get_all_clients()
    assert len(clients) == 0

def test_delete_passerelle(db_connection):
    """
    Test de suppression d'une passerelle.
    Vérifie que la passerelle est correctement supprimée de la base de données.
    """
    database.add_passerelle("test_passerelle")
    passerelles = database.get_all_passerelles()
    assert len(passerelles) == 1
    id_passerelle = passerelles[0]['IdPasserelle']
    database.delete_passerelle(id_passerelle)
    passerelles = database.get_all_passerelles()
    assert len(passerelles) == 0

def test_delete_logiciel(db_connection):
    """
    Test de suppression d'un logiciel.
    Vérifie que le logiciel est correctement supprimé de la base de données.
    """
    database.add_logiciel("test_logiciel")
    logiciels = database.get_all_logiciels()
    assert len(logiciels) == 1
    id_logiciel = logiciels[0]['IdLogiciel']
    database.delete_logiciel(id_logiciel)
    logiciels = database.get_all_logiciels()
    assert len(logiciels) == 0

def test_delete_champ(db_connection):
    """
    Test de suppression d'un champ.
    Vérifie que le champ est correctement supprimé de la base de données.
    """
    database.add_champ("test_champ", "test_table")
    champs = database.get_all_champs()
    assert len(champs) == 1
    id_champ = champs[0]['IdChamp']
    database.delete_champ(id_champ)
    champs = database.get_all_champs()
    assert len(champs) == 0

def test_delete_connecteur(db_connection):
    """
    Test de suppression d'un connecteur.
    Vérifie que le connecteur est correctement supprimé de la base de données.
    """
    database.add_logiciel("test_logiciel")
    database.add_passerelle("test_passerelle")
    id_logiciel = database.get_id_logiciel_by_lib_logiciel("test_logiciel")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_connecteur(id_logiciel, id_passerelle, True)
    connecteurs = database.get_all_connecteurs()
    assert len(connecteurs) == 1
    database.delete_connecteur(id_logiciel, id_passerelle)
    connecteurs = database.get_all_connecteurs()
    assert len(connecteurs) == 0

def test_delete_champ_passerelle(db_connection):
    """
    Test de suppression d'un champ passerelle.
    Vérifie que le champ passerelle est correctement supprimé de la base de données.
    """
    database.add_client("test_user")
    database.add_passerelle("test_passerelle")
    id_client = database.get_id_client_by_lib_client("test_user")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_passerelle_client(id_passerelle, id_client)
    passerelle_clients = database.get_all_passerelle_client()
    id_passerelle_client = passerelle_clients[0]['IdPasserelleClient']
    database.add_champ("test_champ", "test_table")
    id_champ = database.get_id_champ_by_lib_champ("test_champ")
    database.add_champ_passerelle(id_passerelle_client, id_champ, "test_value")
    champ_passerelles = database.get_all_champ_passerelle()
    assert len(champ_passerelles) == 1
    database.delete_champ_passerelle(id_champ, id_passerelle_client)
    champ_passerelles = database.get_all_champ_passerelle()
    assert len(champ_passerelles) == 0

def test_add_and_get_passerelle_client(db_connection):
    """
    Test d'ajout d'une passerelle client et de récupération par identifiant.
    Vérifie que la passerelle client est correctement ajoutée et récupérée.
    """
    database.add_client("test_user")
    database.add_passerelle("test_passerelle")
    id_client = database.get_id_client_by_lib_client("test_user")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_passerelle_client(id_passerelle, id_client)
    passerelle_clients = database.get_all_passerelle_client()
    assert len(passerelle_clients) == 1
    assert passerelle_clients[0]['IdClient'] == id_client
    assert passerelle_clients[0]['IdPasserelle'] == id_passerelle

def test_get_passerelle_client_with_lib_passerelle(db_connection):
    """
    Test de récupération des passerelles associées à un client spécifique avec le libellé de la passerelle.
    Vérifie que les passerelles sont correctement récupérées avec leur libellé.
    """
    database.add_client("test_user")
    database.add_passerelle("test_passerelle")
    id_client = database.get_id_client_by_lib_client("test_user")
    id_passerelle = database.get_id_passerelle_by_lib_passerelle("test_passerelle")
    database.add_passerelle_client(id_passerelle, id_client)
    passerelle_clients = database.get_passerelle_client_with_lib_passerelle(id_client)
    assert len(passerelle_clients) == 1
    assert passerelle_clients[0]['LibPasserelle'] == "test_passerelle"
