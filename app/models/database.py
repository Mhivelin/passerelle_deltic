"""
Ce module contient des fonctions pour interagir avec la base de données SQLite.

voici le script de création de la base de données :

CREATE TABLE CLIENT(
   idClient INTEGER,
   username TEXT NOT NULL,
   PRIMARY KEY(idClient)
);

CREATE TABLE LOGICIEL(
   IdLogiciel INTEGER,
   LibLogiciel TEXT NOT NULL,
   PRIMARY KEY(IdLogiciel)
);

CREATE TABLE PASSERELLE(
   IdPasserelle INTEGER,
   LibPasserelle TEXT NOT NULL,
   PRIMARY KEY(IdPasserelle)
);


CREATE TABLE Connecte_Logiciel_Source(
   IdPasserelle INTEGER,
   IdLogiciel INTEGER NOT NULL,
   PRIMARY KEY(IdPasserelle, IdLogiciel),
   FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
   FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
);

CREATE TABLE Connecte_Logiciel_Destination(
   IdPasserelle INTEGER,
   IdLogiciel INTEGER NOT NULL,
   PRIMARY KEY(IdPasserelle, IdLogiciel),
   FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
   FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
);

CREATE TABLE CLIENT_PASSERELLE(
   idClient INTEGER,
   IdPasserelle INTEGER,
   PRIMARY KEY(idClient, IdPasserelle),
   FOREIGN KEY(idClient) REFERENCES CLIENT(idClient),
   FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle)
);

CREATE TABLE REQUIERT(
   IdLogiciel INTEGER,
   IdPasserelle INTEGER,
   id_champ INTEGER NOT NULL,
   PRIMARY KEY(id_champ, IdLogiciel, IdPasserelle),
   FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel),
   FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
   FOREIGN KEY(id_champ) REFERENCES CHAMP(id_champ),
   CHECK (
       (IdLogiciel IS NOT NULL AND IdPasserelle IS NULL) OR
       (IdLogiciel IS NULL AND IdPasserelle IS NOT NULL)
   )
);

CREATE TABLE CHAMP(
   id_champ INTEGER NOT NULL,
   lib_champ TET NOT NULL,
   nomTable TEXT NOT NULL,
   PRIMARY KEY(id_champ)
);


CREATE TABLE CHAMP_CLIENT(
   idClient INTEGER,
   id_champ INTEGER,
   valeur TEXT NOT NULL,
   PRIMARY KEY(idClient, id_champ),
   FOREIGN KEY(idClient) REFERENCES CLIENT(idClient),
   FOREIGN KEY(id_champ) REFERENCES CHAMPS(id_champ)
);





"""


import sqlite3


#########################################################################################
#                            Connexion à la base de données                             #
#########################################################################################


def get_db_connexion():
    """Retourne une connexion à la base de données SQLite."""
    conn = sqlite3.connect("BDPasserelleV2.db")
    conn.row_factory = sqlite3.Row
    return conn


#############################################################################################
#                                        CREATE DATABASE                                    #
#############################################################################################


def create_database():
    """
    Crée les tables nécessaires dans la base de données si elles n'existent pas déjà.

    Cette fonction exécute une série d'instructions SQL pour créer les tables suivantes :
    - CLIENT
    - LOGICIEL
    - PASSERELLE
    - Connecte_Logiciel_Source
    - Connecte_Logiciel_Destination
    - CLIENT_PASSERELLE
    - CHAMP
    - REQUIERT
    - CHAMP_CLIENT


    Si l'une des tables existe déjà, l'instruction CREATE TABLE correspondante est ignorée.

    Returns:
        None
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    # Creation des tables

    # CLIENT
    if not execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='CLIENT';"):
        cursor.execute(
            """
            CREATE TABLE CLIENT(
                idClient INTEGER,
                username TEXT NOT NULL,
                PRIMARY KEY(idClient)
            );""")

    # LOGICIEL
    if not execute_query("SELECT name FROM sqlite_master WHERE type='table' AND name='LOGICIEL';"):
        cursor.execute(
            """
            CREATE TABLE LOGICIEL(
                IdLogiciel INTEGER,
                LibLogiciel TEXT NOT NULL,
                PRIMARY KEY(IdLogiciel)
            );""")

    # PASSERELLE
    if not execute_query("""
                         SELECT name
                         FROM sqlite_master
                         WHERE type='table'
                         AND name='PASSERELLE';"""):
        cursor.execute(
            """
            CREATE TABLE PASSERELLE(
                IdPasserelle INTEGER,
                LibPasserelle TEXT NOT NULL,
                PRIMARY KEY(IdPasserelle)
            );""")


    # Connecte_Logiciel_Source
    if not execute_query("""SELECT name
                         FROM sqlite_master
                         WHERE type='table'
                         AND name='Connecte_Logiciel_Source';"""):
        cursor.execute(
            """
            CREATE TABLE Connecte_Logiciel_Source(
                IdConnecteur INTEGER,
                IdPasserelle INTEGER,
                IdLogiciel INTEGER NOT NULL,
                PRIMARY KEY(idConnecteur),
                FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
                FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
            );""")

    # Connecte_Logiciel_Destination
    if not execute_query("""SELECT name
                         FROM sqlite_master
                         WHERE type='table'
                         AND name='Connecte_Logiciel_Destination';"""):
        cursor.execute(
            """
            CREATE TABLE Connecte_Logiciel_Destination(
                IdConnecteur INTEGER,
                IdPasserelle INTEGER,
                IdLogiciel INTEGER NOT NULL,
                PRIMARY KEY(idConnecteur),
                FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
                FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
            );""")

    # CLIENT_PASSERELLE
    if not execute_query("""SELECT name
                         FROM sqlite_master
                         WHERE type='table'
                         AND name='CLIENT_PASSERELLE';"""):
        cursor.execute(
            """
            CREATE TABLE CLIENT_PASSERELLE(
                idClient INTEGER,
                IdPasserelle INTEGER,
                PRIMARY KEY(idClient, IdPasserelle),
                FOREIGN KEY(idClient) REFERENCES CLIENT(idClient),
                FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle)
            );""")

    # CHAMP
    if not execute_query("""SELECT name
                            FROM sqlite_master
                            WHERE type='table'
                            AND name='CHAMP';"""):
        cursor.execute(
            """
            CREATE TABLE CHAMP(
                id_champ INTEGER NOT NULL,
                lib_champ TEXT NOT NULL,
                nomTable TEXT NOT NULL,
                PRIMARY KEY(id_champ)
            );""")

    # REQUIERT
    if not execute_query("""SELECT name
                            FROM sqlite_master
                            WHERE type='table'
                            AND name='REQUIERT';"""):
        cursor.execute(
            """
            CREATE TABLE REQUIERT(
                IdLogiciel INTEGER,
                IdPasserelle INTEGER,
                id_champ INTEGER NOT NULL,
                PRIMARY KEY(id_champ, IdLogiciel, IdPasserelle),
                FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel),
                FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
                FOREIGN KEY(id_champ) REFERENCES CHAMP(id_champ),
                CHECK (
                    (IdLogiciel IS NOT NULL AND IdPasserelle IS NULL) OR
                    (IdLogiciel IS NULL AND IdPasserelle IS NOT NULL)
                )
            );""")



    # CHAMP_CLIENT
    if not execute_query("""SELECT name
                            FROM sqlite_master
                            WHERE type='table'
                            AND name='CHAMP_CLIENT';"""):
        cursor.execute(
            """
            CREATE TABLE CHAMP_CLIENT(
                idClient INTEGER,
                id_champ INTEGER,
                valeur TEXT NOT NULL,
                PRIMARY KEY(idClient, id_champ),
                FOREIGN KEY(idClient) REFERENCES CLIENT(idClient),
                FOREIGN KEY(id_champ) REFERENCES CHAMP(id_champ)
            );""")





    conn.commit()
    conn.close()





def execute_query(query, params=None):
    """Exécute une requête SQL sur la base de données et retourne les résultats
    si la requête est un SELECT."""
    conn = get_db_connexion()



    try:
        cursor = conn.cursor()
        if params:
            # Nettoie les paramètres de la requête
            params = tuple(params)
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if not query.strip().upper().startswith("SELECT"):
            conn.commit()

        # Récupère les résultats seulement pour les requêtes SELECT
        # (pas besoin pour les INSERT, UPDATE, DELETE, etc.)
        if query.strip().upper().startswith("SELECT"):
            # transforme les résultats en json
            result = [dict(row) for row in cursor.fetchall()]
            return result


    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def execute_query_single(query, params=None):
    """Exécute une requête SQL sur la base de données et retourne un seul résultat si la
    requête est un SELECT."""
    conn = get_db_connexion()

    try:
        if params:
            result = conn.execute(query, params).fetchone()
        else:
            result = conn.execute(query).fetchone()
        conn.commit()

        # transforme les résultats en json
        if result:
            result = dict(result)



        return result
    except Exception as e:
        return e
    finally:
        conn.close()


def add_record(table_name, columns, values):
    """Ajoute un enregistrement à la table spécifiée avec les colonnes et valeurs spécifiées."""
    query = f"""INSERT INTO {table_name}({', '.join(columns)})
    VALUES ({', '.join(['?'] * len(values))})"""
    return execute_query(query, values)


def delete_record(table_name, condition, params):
    """Supprime un enregistrement de la table spécifiée en fonction de
    la condition et des paramètres spécifiés."""
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return execute_query(query, params)


def get_all_records(table_name):
    """Récupère tous les enregistrements de la table spécifiée."""
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)


def get_record_by_id(table_name, id_column, id_value):
    """Récupère un enregistrement spécifique de la table spécifiée en fonction de
    la colonne et de la valeur d'identifiant."""
    query = f"SELECT * FROM {table_name} WHERE {id_column} = ?"
    return execute_query_single(query, (id_value, ))


def drop_table(table_name):
    """Supprime la table spécifiée de la base de données."""
    query = f"DROP TABLE IF EXISTS {table_name}"
    return execute_query(query)


###################################################################################################
#                                        PASSERELLE                                              #
###################################################################################################


def get_all_passerelles():
    """Récupère toutes les passerelles de la base de données."""

    return get_all_records("PASSERELLE")


def get_passerelle_by_id(id_passerelle):
    """Récupère une passerelle spécifique en fonction de son identifiant."""

    return get_record_by_id("PASSERELLE", "IdPasserelle", id_passerelle)


def get_id_passerelle_by_lib_passerelle(lib_passerelle):
    """Récupère une passerelle spécifique en fonction de son libellé."""

    query = """SELECT IdPasserelle FROM PASSERELLE WHERE LibPasserelle = ?"""
    return execute_query_single(query, (lib_passerelle, ))["IdPasserelle"]




def delete_passerelle(id_passerelle):
    """Supprime une passerelle spécifique en fonction de son identifiant."""

    return delete_record("PASSERELLE", "IdPasserelle = ?", (id_passerelle, ))

def get_passerelle_by_logiciel(logiciel_id):
    """Récupère toutes les passerelles associées à un logiciel spécifique."""
    query = """
        SELECT DISTINCT p.*
        FROM (
            SELECT IdPasserelle
            FROM Connecte_Logiciel_Source
            WHERE IdLogiciel = ?

            UNION

            SELECT IdPasserelle
            FROM Connecte_Logiciel_Destination
            WHERE IdLogiciel = ?
        ) AS pass_ids
        JOIN PASSERELLE AS p ON pass_ids.IdPasserelle = p.IdPasserelle
    """
    return execute_query(query, (logiciel_id, logiciel_id))


def get_passerelle_by_client(client_id):
    """Récupère toutes les passerelles associées à un client spécifique."""
    query = """
        SELECT DISTINCT p.*
        FROM (
            SELECT IdPasserelle
            FROM CLIENT_PASSERELLE
            WHERE idClient = ?
        ) AS pass_ids
        JOIN PASSERELLE AS p ON pass_ids.IdPasserelle = p.IdPasserelle
    """
    return execute_query(query, (client_id, ))

def get_passerelle_with_connectors_by_id(id_passerelle):
    """Récupère une passerelle spécifique avec ses connecteurs source et destination."""
    passerelle = get_passerelle_by_id(id_passerelle)
    if passerelle:
        passerelle["ConnecteursSource"] = get_connecteur_source_by_id(id_passerelle)
        passerelle["ConnecteursDestination"] = get_connecteur_destination_by_id(id_passerelle)
    return passerelle



def add_passerelle_with_connectors(lib_passerelle, source_logiciel_id, destination_logiciel_id):
    """Ajoute une passerelle avec des connecteurs source et destination spécifiés.
    note: REQUIERT des logiciels existants dans la base de données.
    """
    try:
        # Ajouter la passerelle
        add_passerelle(lib_passerelle)
        passerelle_id = get_id_passerelle_by_lib_passerelle(lib_passerelle)

        # Ajouter les connecteurs source et destination
        if passerelle_id:
            add_connecteur_source(passerelle_id, source_logiciel_id)
            add_connecteur_destination(passerelle_id, destination_logiciel_id)

        return passerelle_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def add_passerelle(lib_passerelle):
    """Ajoute une passerelle avec le libellé spécifié."""
    return add_record("PASSERELLE", ["LibPasserelle"], [lib_passerelle])

def add_connecteur_source(passerelle_id, logiciel_id):
    """Ajoute un connecteur source pour une passerelle spécifique et un logiciel spécifique."""
    return add_record("Connecte_Logiciel_Source",
                      ["IdPasserelle",
                       "IdLogiciel"],
                      [passerelle_id,
                       logiciel_id])

def add_connecteur_destination(passerelle_id, logiciel_id):
    """Ajoute un connecteur de destination pour une passerelle spécifique et un
    logiciel spécifique."""
    return add_record("Connecte_Logiciel_Destination",
                      ["IdPasserelle", "IdLogiciel"],
                      [passerelle_id, logiciel_id])

def delete_connecteur_source(passerelle_id):
    """Supprime un connecteur source pour une passerelle spécifique."""
    return delete_record("Connecte_Logiciel_Source", "IdPasserelle = ?", (passerelle_id, ))

def delete_connecteur_destination(passerelle_id):
    """Supprime un connecteur de destination pour une passerelle spécifique."""
    return delete_record("Connecte_Logiciel_Destination", "IdPasserelle = ?", (passerelle_id, ))

def get_all_connecteurs_source():
    """Récupère tous les connecteurs source de la base de données."""
    return get_all_records("Connecte_Logiciel_Source")

def get_all_connecteurs_destination():
    """Récupère tous les connecteurs de destination de la base de données."""
    return get_all_records("Connecte_Logiciel_Destination")

def get_connecteur_source_by_id(passerelle_id):
    """Récupère un connecteur source pour une passerelle spécifique."""
    query = "SELECT * FROM Connecte_Logiciel_Source WHERE IdPasserelle = ?"
    return execute_query_single(query, (passerelle_id, ))

def get_connecteur_destination_by_id(passerelle_id):
    """Récupère un connecteur de destination pour une passerelle spécifique."""
    query = "SELECT * FROM Connecte_Logiciel_Destination WHERE IdPasserelle = ?"
    return execute_query_single(query, (passerelle_id, ))




##########################################################################################
#                                       CLIENT                                          #
##########################################################################################


def get_all_clients():
    """Récupère tous les clients de la base de données."""
    return get_all_records("CLIENT")

def get_client_by_id(id_client):
    """Récupère un client spécifique en fonction de son identifiant."""
    return get_record_by_id("CLIENT", "idClient", id_client)

def get_id_client_by_lib_client(lib_client):
    """Récupère un client spécifique en fonction de son libellé."""
    query = "SELECT idClient FROM CLIENT WHERE username = ?"
    return execute_query_single(query, (lib_client, ))["idClient"]

def add_client(username):
    """Ajoute un client avec le nom d'utilisateur spécifié."""
    return add_record("CLIENT", ["username"], [username])

def delete_client(id_client):
    """Supprime un client spécifique en fonction de son identifiant."""
    return delete_record("CLIENT", "idClient = ?", (id_client, ))

def get_client_by_logiciel(logiciel_id):
    """Récupère tous les clients associés à un logiciel spécifique."""
    query = """
        SELECT DISTINCT c.*
        FROM (
            SELECT idClient
            FROM LOGICIEL_CLIENT
            WHERE IdLogiciel = ?
        ) AS client_ids
        JOIN CLIENT AS c ON client_ids.idClient = c.idClient
    """
    return execute_query(query, (logiciel_id, ))

def get_client_by_passerelle(passerelle_id):
    """Récupère tous les clients associés à une passerelle spécifique."""
    query = """
        SELECT DISTINCT c.*
        FROM (
            SELECT idClient
            FROM CLIENT_PASSERELLE
            WHERE IdPasserelle = ?
        ) AS client_ids
        JOIN CLIENT AS c ON client_ids.idClient = c.idClient
    """
    return execute_query(query, (passerelle_id, ))

def get_client_passerelle():
    """Récupère les passerelles clients."""
    query = """
        SELECT CLIENT_PASSERELLE.idClient, CLIENT_PASSERELLE.IdPasserelle
        FROM CLIENT_PASSERELLE
    """
    return execute_query(query)



def add_client_passerelle(id_client, id_passerelle):
    """Ajoute un client à une passerelle spécifique."""
    return add_record("CLIENT_PASSERELLE", ["idClient", "IdPasserelle"], [id_client, id_passerelle])

def delete_client_passerelle(id_client, id_passerelle):
    """Supprime un client d'une passerelle spécifique."""
    return delete_record("CLIENT_PASSERELLE",
                         "idClient = ? AND IdPasserelle = ?",
                         (id_client, id_passerelle))

def get_client_passerelle_by_id(id_client, id_passerelle):
    """Récupère un client de passerelle spécifique en fonction de l'identifiant du client et de
    l'identifiant de la passerelle."""
    query = "SELECT * FROM CLIENT_PASSERELLE WHERE idClient = ? AND IdPasserelle = ?"
    return execute_query_single(query, (id_client, id_passerelle))


def get_passerelle_client_by_client(client_id):
    """Récupère idClient IdPasserelle et LibPasserelle par idClient"""
    query = """
        SELECT CLIENT_PASSERELLE.idClient, CLIENT_PASSERELLE.IdPasserelle, PASSERELLE.LibPasserelle
        FROM CLIENT_PASSERELLE
        JOIN PASSERELLE ON CLIENT_PASSERELLE.IdPasserelle = PASSERELLE.IdPasserelle
        WHERE CLIENT_PASSERELLE.idClient = ?
    """



    return execute_query(query, (client_id, ))




#############################################################################################
#                                       LOGICIEL                                           #
#############################################################################################


def get_all_logiciels():
    """Récupère tous les logiciels de la base de données."""
    return get_all_records("LOGICIEL")


def get_logiciel_by_id(id_logiciel):
    """Récupère un logiciel spécifique en fonction de son identifiant."""
    return get_record_by_id("LOGICIEL", "IdLogiciel", id_logiciel)


def get_id_logiciel_by_lib_logiciel(lib_logiciel):
    """Récupère un logiciel spécifique en fonction de son libellé."""
    query = "SELECT IdLogiciel FROM LOGICIEL WHERE LibLogiciel = ?"
    return execute_query_single(query, (lib_logiciel, ))["IdLogiciel"]


def add_logiciel(lib_logiciel):
    """Ajoute un logiciel avec le libellé spécifié."""
    return add_record("LOGICIEL", ["LibLogiciel"], [lib_logiciel])


def delete_logiciel(id_logiciel):
    """Supprime un logiciel spécifique en fonction de son identifiant."""
    return delete_record("LOGICIEL", "IdLogiciel = ?", (id_logiciel, ))


def get_logiciel_by_passerelle(passerelle_id):
    """Récupère tous les logiciels associés à une passerelle spécifique."""
    query = """
        SELECT DISTINCT l.*
        FROM (
            SELECT IdLogiciel
            FROM Connecte_Logiciel_Source
            WHERE IdPasserelle = ?

            UNION

            SELECT IdLogiciel
            FROM Connecte_Logiciel_Destination
            WHERE IdPasserelle = ?
        ) AS logiciel_ids
        JOIN LOGICIEL AS l ON logiciel_ids.IdLogiciel = l.IdLogiciel
    """
    return execute_query(query, (passerelle_id, passerelle_id))







############################################################################################
#                                   CHAMP                                                   #
############################################################################################


def get_all_champs():
    """Récupère tous les champs de la base de données."""
    return get_all_records("CHAMP")

def get_champ_by_id(id_champ):
    """Récupère un champ spécifique en fonction de son identifiant."""
    return get_record_by_id("CHAMP", "id_champ", id_champ)

def get_id_champ_by_lib_champ(lib_champ):
    """Récupère un champ spécifique en fonction de son libellé."""
    query = "SELECT id_champ FROM CHAMP WHERE lib_champ = ?"
    return execute_query_single(query, (lib_champ, ))["id_champ"]

def add_champ(lib_champ, nom_table):
    """Ajoute un champ avec le libellé et le nom de table spécifiés."""
    return add_record("CHAMP", ["lib_champ", "nomTable"], [lib_champ, nom_table])

def delete_champ(id_champ):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_record("CHAMP", "id_champ = ?", (id_champ, ))

def get_champ_by_logiciel(logiciel_id):
    """Récupère tous les champs associés à un logiciel spécifique."""
    query = """
        SELECT c.*
        FROM CHAMP AS c
        JOIN REQUIERT AS r ON c.id_champ = r.id_champ
        WHERE r.IdLogiciel = ?
    """
    return execute_query(query, (logiciel_id, ))

def get_champ_by_passerelle(passerelle_id):
    """Récupère tous les champs associés à une passerelle spécifique."""
    query = """
        SELECT c.*
        FROM CHAMP AS c
        JOIN REQUIERT AS r ON c.id_champ = r.id_champ
        WHERE r.IdPasserelle = ?
    """
    return execute_query(query, (passerelle_id, ))

def get_champ_by_client(client_id):
    """Récupère tous les champs associés à un client selon les passerelles et donc les logiciels associés."""
    query = """
        SELECT DISTINCT c.lib_champ, c.id_champ
        FROM CLIENT cl
        JOIN CLIENT_PASSERELLE cp ON cl.idClient = cp.idClient
        JOIN PASSERELLE p ON cp.IdPasserelle = p.IdPasserelle
        LEFT JOIN Connecte_Logiciel_Source cls ON p.IdPasserelle = cls.IdPasserelle
        LEFT JOIN Connecte_Logiciel_Destination cld ON p.IdPasserelle = cld.IdPasserelle
        JOIN LOGICIEL l ON l.IdLogiciel = COALESCE(cls.IdLogiciel, cld.IdLogiciel)
        JOIN REQUIERT r ON l.IdLogiciel = r.IdLogiciel
        JOIN CHAMP c ON r.id_champ = c.id_champ
        WHERE cl.idClient = ?
    """
    return execute_query(query, (client_id, ))









############################################################################################
#                                   REQUIERT                                                #
############################################################################################


def get_all_requiert():
    """Récupère tous les champs de la base de données."""
    return get_all_records("REQUIERT")

def get_requiert_by_id(id_champ, id_logiciel, id_passerelle):
    """Récupère un champ spécifique en fonction de son identifiant."""
    query = "SELECT * FROM REQUIERT WHERE id_champ = ? AND IdLogiciel = ? AND IdPasserelle = ?"
    return execute_query_single(query, (id_champ, id_logiciel, id_passerelle))

def get_requiert_logiciel_by_id(id_champ, id_logiciel):
    """Récupère un champ spécifique en fonction de son identifiant."""
    return get_requiert_by_id(id_champ, id_logiciel, None)

def get_requiert_passerelle_by_id(id_champ, id_passerelle):
    """Récupère un champ spécifique en fonction de son identifiant."""
    return get_requiert_by_id(id_champ, None, id_passerelle)

def add_requiert(id_champ, id_logiciel, id_passerelle):
    """Ajoute un champ avec le libellé et le nom de table spécifiés."""
    return add_record("REQUIERT", ["id_champ", "IdLogiciel", "IdPasserelle"], [id_champ, id_logiciel, id_passerelle])

def add_requiert_logiciel(id_champ, id_logiciel):
    """Ajoute un champ avec le libellé et le nom de table spécifiés."""
    return add_requiert(id_champ, id_logiciel, None)

def add_requiert_passerelle(id_champ, id_passerelle):
    """Ajoute un champ avec le libellé et le nom de table spécifiés."""
    return add_requiert(id_champ, None, id_passerelle)

def delete_requiert(id_champ, id_logiciel, id_passerelle):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_record("REQUIERT", "id_champ = ? AND IdLogiciel = ? AND IdPasserelle = ?", (id_champ, id_logiciel, id_passerelle))

def delete_requiert_logiciel(id_champ, id_logiciel):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_requiert(id_champ, id_logiciel, None)

def delete_requiert_passerelle(id_champ, id_passerelle):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_requiert(id_champ, None, id_passerelle)

def get_requiert_by_logiciel(logiciel_id):
    """Récupère tous les champs associés à un logiciel spécifique."""
    query = "SELECT * FROM REQUIERT WHERE IdLogiciel = ?"
    return execute_query(query, (logiciel_id, ))

def get_requiert_by_passerelle(passerelle_id):
    """Récupère tous les champs associés à une passerelle spécifique."""
    query = "SELECT * FROM REQUIERT WHERE IdPasserelle = ?"
    return execute_query(query, (passerelle_id, ))

def get_requiert_by_client(client_id):
    """Récupère tous les champs associés à un client (et donc à ses passerelles et logiciels associés)."""
    query = """

        SELECT DISTINCT c.id_champ, c.lib_champ
        FROM CLIENT cl
        JOIN CLIENT_PASSERELLE cp ON cl.idClient = cp.idClient
        JOIN PASSERELLE p ON cp.IdPasserelle = p.IdPasserelle
        LEFT JOIN Connecte_Logiciel_Source cls ON p.IdPasserelle = cls.IdPasserelle
        LEFT JOIN Connecte_Logiciel_Destination cld ON p.IdPasserelle = cld.IdPasserelle
        JOIN LOGICIEL l ON l.IdLogiciel = COALESCE(cls.IdLogiciel, cld.IdLogiciel)
        JOIN REQUIERT r ON (r.IdLogiciel = l.IdLogiciel OR r.IdPasserelle = p.IdPasserelle)
        JOIN CHAMP c ON r.id_champ = c.id_champ
        WHERE cl.idClient = ?;



    """
    return execute_query(query, (client_id, ))


def get_requiert_by_passerelle_and_his_logiciel(passerelle_id):
    """Récupère tous les champs ainsi que leur lib associés à une passerelle ainsi que les champs associés à son logiciel."""
    query = """
        SELECT DISTINCT r.id_champ, c.lib_champ
        FROM REQUIERT r
        JOIN CHAMP c ON r.id_champ = c.id_champ
        WHERE r.IdPasserelle = ?

        UNION

        SELECT DISTINCT r.id_champ, c.lib_champ
        FROM REQUIERT r
        JOIN CHAMP c ON r.id_champ = c.id_champ
        JOIN Connecte_Logiciel_Source cls ON r.IdLogiciel = cls.IdLogiciel
        WHERE cls.IdPasserelle = ?

        UNION

        SELECT DISTINCT r.id_champ, c.lib_champ
        FROM REQUIERT r
        JOIN CHAMP c ON r.id_champ = c.id_champ
        JOIN Connecte_Logiciel_Destination cld ON r.IdLogiciel = cld.IdLogiciel
        WHERE cld.IdPasserelle = ?


    """
    return execute_query(query, (passerelle_id, passerelle_id, passerelle_id))


def get_all_fields_requiert_by_client(client_id):
    """Récupère tous les champs associés à un client (et donc à ses passerelles et logiciels associés)."""
    query = """
        SELECT DISTINCT champ.id_champ, champ.lib_champ
        FROM CLIENT client
        JOIN CLIENT_PASSERELLE cp ON client.idClient = cp.idClient
        JOIN PASSERELLE passerelle ON cp.IdPasserelle = passerelle.IdPasserelle
        JOIN REQUIERT rq ON passerelle.IdPasserelle = rq.IdPasserelle OR rq.IdLogiciel IN (
            SELECT cls.IdLogiciel
            FROM Connecte_Logiciel_Source cls
            WHERE cls.IdPasserelle = passerelle.IdPasserelle

            UNION

            SELECT cld.IdLogiciel
            FROM Connecte_Logiciel_Destination cld
            WHERE cld.IdPasserelle = passerelle.IdPasserelle
        )
        JOIN CHAMP champ ON rq.id_champ = champ.id_champ
        WHERE client.idClient = ?
    """
    return execute_query(query, (client_id, ))








############################################################################################
#                                   CHAMP_CLIENT                                            #
############################################################################################


def get_all_champs_clients():
    """Récupère tous les champs de la base de données."""
    return get_all_records("CHAMP_CLIENT")

def get_champ_client_by_id(id_client, id_champ):
    """Récupère un le nom et la valeur d'un champ spécifique en fonction de son identifiant."""
    query = "SELECT * FROM CHAMP_CLIENT WHERE idClient = ? AND id_champ = ?"
    return execute_query_single(query, (id_client, id_champ))

def get_champ_client_by_client(client_id):
    """Récupère tous les champs associés à un client spécifique."""
    query = "SELECT * FROM CHAMP_CLIENT JOIN CHAMP ON CHAMP_CLIENT.id_champ = CHAMP.id_champ WHERE idClient = ?"
    return execute_query(query, (client_id, ))

def get_champ_client_by_label(label, client_id):
    """Récupère le champ d'un client spécifique en fonction de son libellé."""
    query = """
        SELECT cc.*
        FROM CHAMP_CLIENT AS cc
        JOIN CHAMP AS c ON cc.id_champ = c.id_champ
        WHERE c.lib_champ = ? AND cc.idClient = ?
    """
    return execute_query_single(query, (label, client_id))



def get_champ_client_by_champ(champ_id):
    """Récupère tous les champs associés à un champ spécifique."""
    query = "SELECT * FROM CHAMP_CLIENT WHERE id_champ = ?"
    return execute_query(query, (champ_id, ))

def add_champ_client(id_client, id_champ, valeur):
    """Ajoute un champ avec le libellé et le nom de table spécifiés.
    si le champ existe déjà, il est mis à jour avec la nouvelle valeur."""
    if get_champ_client_by_id(id_client, id_champ):
        query = """
            UPDATE CHAMP_CLIENT
            SET valeur = ?
            WHERE idClient = ? AND id_champ = ?
        """
        return execute_query(query, (valeur, id_client, id_champ))
    else:
        return add_record("CHAMP_CLIENT", ["idClient", "id_champ", "valeur"], [id_client, id_champ, valeur])




def delete_champ_client(id_client, id_champ):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_record("CHAMP_CLIENT", "idClient = ? AND id_champ = ?", (id_client, id_champ))

def delete_champ_client_libelle(id_client, lib_champ):
    """Supprime un champ spécifique en fonction de son identifiant."""
    query = """
        DELETE FROM CHAMP_CLIENT
        WHERE idClient = ? AND id_champ = (
            SELECT id_champ
            FROM CHAMP
            WHERE lib_champ = ?
        )
    """
    return execute_query(query, (id_client, lib_champ))











#######################################################################################
#                               Requête plus complexe                                 #
#######################################################################################




def drop_all_tables():
    """ Supprime toutes les tables de la base de données."""
    drop_table("CLIENT")
    drop_table("LOGICIEL")
    drop_table("PASSERELLE")
    drop_table("Connecte_Logiciel_Source")
    drop_table("Connecte_Logiciel_Destination")
    drop_table("CLIENT_PASSERELLE")
    drop_table("REQUIERT")
    drop_table("CHAMP")
    drop_table("CHAMP_CLIENT")
    drop_table("requiert")