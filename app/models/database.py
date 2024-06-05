import sqlite3

#########################################################################################
#                            Connexion à la base de données                             #
#########################################################################################

def get_db_connexion():
    """Retourne une connexion à la base de données SQLite."""
    conn = sqlite3.connect("instance/database.db")
    conn.row_factory = sqlite3.Row
    return conn

#############################################################################################
#                                        CREATE DATABASE                                    #
#############################################################################################

def create_database():
    """
    Crée les tables nécessaires dans la base de données si elles n'existent pas déjà.
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    # Création des tables

    # CLIENT
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CLIENT(
            IdClient INTEGER PRIMARY KEY,
            Username TEXT NOT NULL
        );"""
    )

    # LOGICIEL
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS LOGICIEL(
            IdLogiciel INTEGER PRIMARY KEY,
            LibLogiciel TEXT NOT NULL
        );"""
    )

    # PASSERELLE
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PASSERELLE(
            IdPasserelle INTEGER PRIMARY KEY,
            LibPasserelle TEXT NOT NULL
        );"""
    )

    # CHAMPS
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CHAMPS(
            IdChamp INTEGER PRIMARY KEY,
            LibChamp TEXT NOT NULL,
            NomTable TEXT NOT NULL,
            IdPasserelle INTEGER,
            IdLogiciel INTEGER,
            FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
            FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
        );"""
    )

    # PASSERELLE_CLIENT
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PASSERELLE_CLIENT(
            IdPasserelleClient INTEGER PRIMARY KEY,
            IdPasserelle INTEGER NOT NULL,
            IdClient INTEGER NOT NULL,
            FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
            FOREIGN KEY(IdClient) REFERENCES CLIENT(IdClient)
        );"""
    )

    # CONNECT_LOGICIEL
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CONNECT_LOGICIEL(
            IdLogiciel INTEGER,
            IdPasserelle INTEGER,
            IsSource NUMERIC,
            PRIMARY KEY(IdLogiciel, IdPasserelle),
            FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel),
            FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle)
        );"""
    )

    # CHAMP_PASSERELLE
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CHAMP_PASSERELLE(
            IdChamp INTEGER,
            IdPasserelleClient INTEGER,
            Valeur TEXT,
            PRIMARY KEY(IdChamp, IdPasserelleClient),
            FOREIGN KEY(IdChamp) REFERENCES CHAMPS(IdChamp),
            FOREIGN KEY(IdPasserelleClient) REFERENCES PASSERELLE_CLIENT(IdPasserelleClient)
        );"""
    )

    conn.commit()
    conn.close()

#########################################################################################
#                              FONCTIONS D'EXECUTION DE REQUÊTES                         #
#########################################################################################

def execute_query(query, params=None):
    """Exécute une requête SQL sur la base de données et retourne les résultats si la requête est un SELECT."""
    conn = get_db_connexion()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            result = [dict(row) for row in cursor.fetchall()]
            return result
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

def execute_query_single(query, params=None):
    """Exécute une requête SQL sur la base de données et retourne un seul résultat si la requête est un SELECT."""
    conn = get_db_connexion()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return dict(result)
        conn.commit()
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
    """Supprime un enregistrement de la table spécifiée en fonction de la condition et des paramètres spécifiés."""
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return execute_query(query, params)

def get_all_records(table_name):
    """Récupère tous les enregistrements de la table spécifiée."""
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)

def get_record_by_id(table_name, id_column, id_value):
    """Récupère un enregistrement spécifique de la table spécifiée en fonction de la colonne et de la valeur d'identifiant."""
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
        FROM CONNECT_LOGICIEL cl
        JOIN PASSERELLE p ON cl.IdPasserelle = p.IdPasserelle
        WHERE cl.IdLogiciel = ?
    """
    return execute_query(query, (logiciel_id, ))

def get_passerelle_by_client(client_id):
    """Récupère toutes les passerelles associées à un client spécifique."""
    query = """
        SELECT DISTINCT p.*
        FROM PASSERELLE_CLIENT pc
        JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
        WHERE pc.IdClient = ?
    """
    return execute_query(query, (client_id, ))

def add_passerelle(lib_passerelle):
    """Ajoute une passerelle avec le libellé spécifié."""
    return add_record("PASSERELLE", ["LibPasserelle"], [lib_passerelle])


def add_passerelle_with_logiciels(lib_passerelle, id_logiciel_source, id_logiciel_destination):
    """Ajoute une passerelle avec les logiciels spécifiés."""
    passerelle_id = add_passerelle(lib_passerelle)
    add_connecteur(id_logiciel_source, passerelle_id, True)
    add_connecteur(id_logiciel_destination, passerelle_id, False)



def get_passerelle_by_lib(lib_passerelle):
    """Récupère une passerelle spécifique en fonction de son libellé."""
    query = "SELECT * FROM PASSERELLE WHERE LibPasserelle = ?"
    return execute_query_single(query, (lib_passerelle, ))

###################################################################################################
#                                        CLIENT                                                 #
###################################################################################################

def get_all_clients():
    """Récupère tous les clients de la base de données."""
    return get_all_records("CLIENT")

def get_client_by_id(id_client):
    """Récupère un client spécifique en fonction de son identifiant."""
    return get_record_by_id("CLIENT", "IdClient", id_client)

def get_id_client_by_lib_client(lib_client):
    """Récupère un client spécifique en fonction de son libellé."""
    query = "SELECT IdClient FROM CLIENT WHERE Username = ?"
    return execute_query_single(query, (lib_client, ))["IdClient"]

def add_client(username):
    """Ajoute un client avec le nom d'utilisateur spécifié."""
    return add_record("CLIENT", ["Username"], [username])

def delete_client(id_client):
    """Supprime un client spécifique en fonction de son identifiant."""
    return delete_record("CLIENT", "IdClient = ?", (id_client, ))

###################################################################################################
#                                        LOGICIEL                                               #
###################################################################################################

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

###################################################################################################
#                                        CHAMPS                                                 #
###################################################################################################

def get_all_champs():
    """Récupère tous les champs de la base de données."""
    return get_all_records("CHAMPS")

def get_champ_by_id(id_champ):
    """Récupère un champ spécifique en fonction de son identifiant."""
    return get_record_by_id("CHAMPS", "IdChamp", id_champ)

def get_id_champ_by_lib_champ(lib_champ):
    """Récupère un champ spécifique en fonction de son libellé."""
    query = "SELECT IdChamp FROM CHAMPS WHERE LibChamp = ?"
    res = execute_query_single(query, (lib_champ, ))

    if res is None:
        return None

    return res["IdChamp"]

def add_champ(lib_champ, nom_table, id_passerelle=None, id_logiciel=None):
    """Ajoute un champ avec le libellé et le nom de table spécifiés."""
    columns = ["LibChamp", "NomTable"]
    values = [lib_champ, nom_table]

    if id_passerelle:
        columns.append("IdPasserelle")
        values.append(id_passerelle)

    if id_logiciel:
        columns.append("IdLogiciel")
        values.append(id_logiciel)

    return add_record("CHAMPS", columns, values)


def add_champ_to_passerelle(lib_champ, nom_table, lib_passerelle, id_logiciel=None):
    """Ajoute un champ à une passerelle spécifique."""
    id_passerelle = get_id_passerelle_by_lib_passerelle(lib_passerelle)
    return add_champ(lib_champ, nom_table, id_passerelle, id_logiciel)

def add_champ_to_logiciel(lib_champ, nom_table, lib_logiciel, id_passerelle=None):
    """Ajoute un champ à un logiciel spécifique."""
    id_logiciel = get_id_logiciel_by_lib_logiciel(lib_logiciel)
    return add_champ(lib_champ, nom_table, id_passerelle, id_logiciel)

def delete_champ(id_champ):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_record("CHAMPS", "IdChamp = ?", (id_champ, ))


def get_lib_champ_by_id(id_champ):
    """Récupère le libellé d'un champ spécifique en fonction de son identifiant."""
    query = "SELECT LibChamp FROM CHAMPS WHERE IdChamp = ?"
    return execute_query_single(query, (id_champ, ))["LibChamp"]

###################################################################################################
#                                        CONNECT_LOGICIEL                                       #
###################################################################################################

def get_all_connecteurs():
    """Récupère tous les connecteurs de la base de données."""
    return get_all_records("CONNECT_LOGICIEL")

def get_connecteur_by_id(id_logiciel, id_passerelle):
    """Récupère un connecteur spécifique en fonction de son identifiant."""
    query = "SELECT * FROM CONNECT_LOGICIEL WHERE IdLogiciel = ? AND IdPasserelle = ?"
    return execute_query_single(query, (id_logiciel, id_passerelle))

def add_connecteur(id_logiciel, id_passerelle, is_source):
    """Ajoute un connecteur avec les identifiants logiciel et passerelle spécifiés."""
    return add_record("CONNECT_LOGICIEL", ["IdLogiciel", "IdPasserelle", "IsSource"], [id_logiciel, id_passerelle, is_source])

def delete_connecteur(id_logiciel, id_passerelle):
    """Supprime un connecteur spécifique en fonction de son identifiant."""
    return delete_record("CONNECT_LOGICIEL", "IdLogiciel = ? AND IdPasserelle = ?", (id_logiciel, id_passerelle))

##########################################################################################
#                               CHAMP_PASSERELLE                                        #
##########################################################################################

def add_champ_passerelle(id_passerelle_client, id_champ, valeur):
    """Ajoute un champ passerelle avec l'identifiant, la valeur et IdChamp spécifiés."""
    return add_record("CHAMP_PASSERELLE", ["IdPasserelleClient", "IdChamp", "Valeur"], [id_passerelle_client, id_champ, valeur])

def get_all_champ_passerelle_by_passerelle_client(id_passerelle_client):
    """Récupère tous les champs passerelle associés à une passerelle client spécifique."""
    query = "SELECT * FROM CHAMP_PASSERELLE WHERE IdPasserelleClient = ?"
    return execute_query(query, (id_passerelle_client, ))

def get_all_champ_passerelle_by_passerelle_client_with_lib_champ(id_passerelle_client):
    """Récupère tous les champs passerelle associés à une passerelle client spécifique avec le libellé du champ."""
    query = """
        SELECT CP.*, CH.LibChamp
        FROM CHAMP_PASSERELLE CP
        JOIN CHAMPS CH ON CP.IdChamp = CH.IdChamp
        WHERE IdPasserelleClient = ?
    """
    return execute_query(query, (id_passerelle_client, ))

def update_champ_passerelle(id_passerelle_client, id_champ, valeur):
    """Met à jour un champ passerelle spécifique en fonction de son identifiant."""
    query = "UPDATE CHAMP_PASSERELLE SET Valeur = ? WHERE IdChamp = ? AND IdPasserelleClient = ?"
    return execute_query(query, (valeur, id_champ, id_passerelle_client))


def get_all_champ_passerelle():
    """Récupère tous les champs passerelle de la base de données."""
    return get_all_records("CHAMP_PASSERELLE")

def get_champ_passerelle_by_id(id_champ, id_passerelle_client):
    """Récupère un champ passerelle spécifique en fonction de son identifiant."""
    query = "SELECT * FROM CHAMP_PASSERELLE WHERE IdChamp = ? AND IdPasserelleClient = ?"
    return execute_query_single(query, (id_champ, id_passerelle_client))

def get_champ_passerelle_by_lib_champ(id_passerelle_client, lib_champ):
    """Récupère un champ passerelle spécifique en fonction du libellé du champ."""
    query = """
        SELECT CP.*
        FROM CHAMP_PASSERELLE CP
        JOIN CHAMPS CH ON CP.IdChamp = CH.IdChamp
        WHERE CP.IdPasserelleClient = ? AND CH.LibChamp = ?
    """
    return execute_query_single(query, (id_passerelle_client, lib_champ))

def get_champ_passerelle_by_passerelle_client_and_lib_champ(id_passerelle_client, lib_champ):
    """Récupère un champ passerelle spécifique en fonction du libellé du champ et de l'identifiant de la passerelle client."""
    query = """
        SELECT CP.*
        FROM CHAMP_PASSERELLE CP
        JOIN CHAMPS CH ON CP.IdChamp = CH.IdChamp
        WHERE CP.IdPasserelleClient = ? AND CH.LibChamp = ?
    """
    return execute_query_single(query, (id_passerelle_client, lib_champ))


def delete_champ_passerelle(id_champ, id_passerelle_client):
    """Supprime un champ passerelle spécifique en fonction de son identifiant."""
    return delete_record("CHAMP_PASSERELLE", "IdChamp = ? AND IdPasserelleClient = ?", (id_champ, id_passerelle_client))

def get_champ_passerelle_client_by_client(id_client):
    """Récupère tous les champs passerelle associés à un client spécifique."""
    query = """
        SELECT CP.*
        FROM CHAMP_PASSERELLE CP
        JOIN PASSERELLE_CLIENT PC ON CP.IdPasserelleClient = PC.IdPasserelleClient
        WHERE PC.IdClient = ?
    """
    return execute_query(query, (id_client, ))


def get_champ_passerelle_client_by_client_with_lib_champ(id_client):
    """Récupère tous les champs passerelle associés à un client spécifique avec le libellé du champ."""
    query = """
        SELECT CH.*, CP.Valeur, P.LibPasserelle
        FROM CHAMPS CH
        JOIN CHAMP_PASSERELLE CP ON CH.IdChamp = CP.IdChamp
        JOIN PASSERELLE_CLIENT PC ON CP.IdPasserelleClient = PC.IdPasserelleClient
        JOIN PASSERELLE P ON PC.IdPasserelle = P.IdPasserelle
        WHERE PC.IdClient = ?

    """
    return execute_query(query, (id_client, ))

def add_multiple_champ_passerelle(id_passerelle_client, champs):
    """Ajoute plusieurs champs passerelle à un client spécifique."""
    for champ in champs:
        add_champ_passerelle(id_passerelle_client, champ["IdChamp"], champ["Valeur"])


def add_or_update_champ_passerelle(id_passerelle_client, champs):
    """Ajoute ou met à jour plusieurs champs passerelle à un client spécifique."""
    for champ in champs:
        champ_passerelle = get_champ_passerelle_by_id(champ["IdChamp"], id_passerelle_client)
        if champ_passerelle:
            query = "UPDATE CHAMP_PASSERELLE SET Valeur = ? WHERE IdChamp = ? AND IdPasserelleClient = ?"
            execute_query(query, (champ["Valeur"], champ["IdChamp"], id_passerelle_client))
        else:
            add_champ_passerelle(id_passerelle_client, champ["IdChamp"], champ["Valeur"])



##########################################################################################
#                               PASSERELLE_CLIENT                                       #
##########################################################################################

def add_passerelle_client(id_passerelle, id_client):
    """Ajoute une entrée dans la table PASSERELLE_CLIENT."""
    return add_record("PASSERELLE_CLIENT", ["IdPasserelle", "IdClient"], [id_passerelle, id_client])

def get_all_passerelle_client():
    """Récupère toutes les entrées de la table PASSERELLE_CLIENT."""
    return get_all_records("PASSERELLE_CLIENT")

def get_all_passerelle_client_with_lib_passerelle():
    """Récupère toutes les entrées de la table PASSERELLE_CLIENT avec le libellé de la passerelle."""
    query = """
        SELECT pc.*, p.LibPasserelle
        FROM PASSERELLE_CLIENT pc
        JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
    """
    return execute_query(query)

def get_passerelle_client_by_ids(id_passerelle, id_client):
    """Récupère une entrée spécifique de la table PASSERELLE_CLIENT."""
    query = "SELECT * FROM PASSERELLE_CLIENT WHERE IdPasserelle = ? AND IdClient = ?"
    return execute_query_single(query, (id_passerelle, id_client))

def get_passerelle_client_by_client(id_client):
    """Récupère toutes les passerelles associées à un client spécifique."""
    query = "SELECT * FROM PASSERELLE_CLIENT WHERE IdClient = ?"
    return execute_query(query, (id_client, ))

def get_passerelle_client_with_lib_passerelle(id_client):
    """Récupère toutes les passerelles associées à un client spécifique avec le libellé de la passerelle."""
    query = """
        SELECT pc.*, p.LibPasserelle
        FROM PASSERELLE_CLIENT pc
        JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
        WHERE pc.IdClient = ?
    """
    return execute_query(query, (id_client, ))

def delete_passerelle_client(id_passerelle, id_client):
    """Supprime une entrée spécifique de la table PASSERELLE_CLIENT."""
    return delete_record("PASSERELLE_CLIENT", "IdPasserelle = ? AND IdClient = ?", (id_passerelle, id_client))

##########################################################################################
#                               Requêtes plus complexes                                  #
##########################################################################################

def get_clients_with_passerelles_and_champs():
    """
    Récupère tous les clients avec leurs passerelles associées et les champs des passerelles.
    """
    query = """
        SELECT
            c.IdClient, c.Username,
            p.IdPasserelle, p.LibPasserelle,
            cp.IdChamp, ch.LibChamp, cp.Valeur
        FROM CLIENT c
        LEFT JOIN PASSERELLE_CLIENT pc ON c.IdClient = pc.IdClient
        LEFT JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
        LEFT JOIN CHAMP_PASSERELLE cp ON pc.IdPasserelleClient = cp.IdPasserelleClient
        LEFT JOIN CHAMPS ch ON cp.IdChamp = ch.IdChamp
    """
    return execute_query(query)




def drop_all_tables():
    """Supprime toutes les tables de la base de données."""
    drop_table("CLIENT")
    drop_table("LOGICIEL")
    drop_table("PASSERELLE")
    drop_table("CHAMP_PASSERELLE")
    drop_table("CHAMPS")
    drop_table("CONNECT_LOGICIEL")
    drop_table("PASSERELLE_CLIENT")
