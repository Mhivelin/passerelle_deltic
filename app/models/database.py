"""
Ce fichier contient les fonctions qui permettent de gérer les opérations
sur la base de données.
"""


import sqlite3
import logging
import datetime
# import os

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
            TypeChamp TEXT NOT NULL
            CHECK(TypeChamp IN ('caché',
                'masqué',
                'visible',
                'select_zeendoc_index',
                'select_zeendoc_classeur',
                'select_ebp_folder')),
            FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
            FOREIGN KEY(IdLogiciel) REFERENCES LOGICIEL(IdLogiciel)
        );"""
    )


    # PASSERELLE_CLIENT
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PASSERELLE_CLIENT(
            IdPasserelleClient INTEGER PRIMARY KEY AUTOINCREMENT,
            IdPasserelle INTEGER NOT NULL,
            IdClient INTEGER NOT NULL,
            DateDerSynchronisation DATETIME DEFAULT '1970-01-01',
            FOREIGN KEY(IdPasserelle) REFERENCES PASSERELLE(IdPasserelle),
            FOREIGN KEY(IdClient) REFERENCES CLIENT(IdClient)
        );
        """
    )

    # CONNECT_LOGICIEL
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CONNECT_LOGICIEL(
            IdLogiciel INTEGER,
            IdPasserelle INTEGER,
            IsSource INTEGER,
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
#                              FONCTIONS D'EXECUTION DE REQUÊTES                        #
#########################################################################################

def execute_query(query, params=None):
    """
    Exécute une requête SQL sur la base de données et
    retourne les résultats si la requête est un SELECT.
    """
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
    except sqlite3.DatabaseError as e:
        logging.error("Database error occurred: %s", str(e))
        return None
    except sqlite3.IntegrityError as e:
        logging.error("Integrity error occurred: %s", str(e))
        return None
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))
        return None
    finally:
        conn.close()

def execute_query_single(query, params=None):
    """
    Exécute une requête SQL sur la base de données et retourne
    un seul résultat si la requête est un SELECT.
    """
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
    """
    Supprime un enregistrement de la table spécifiée en
    fonction de la condition et des paramètres spécifiés.
    """
    query = f"DELETE FROM {table_name} WHERE {condition}"
    return execute_query(query, params)

def get_all_records(table_name):
    """Récupère tous les enregistrements de la table spécifiée."""
    query = f"SELECT * FROM {table_name}"
    return execute_query(query)

def get_record_by_id(table_name, id_column, id_value):
    """
    Récupère un enregistrement spécifique de la table spécifiée
    en fonction de la colonne et de la valeur d'identifiant.
    """
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


def get_id_passerelle_by_id_passerelle_client(id_passerelle_client):
    """Récupère une passerelle spécifique en fonction de l'ID de passerelle client."""
    query = "SELECT IdPasserelle FROM PASSERELLE_CLIENT WHERE IdPasserelleClient = ?"
    result = execute_query_single(query, (id_passerelle_client,))

    if result and 'IdPasserelle' in result:
        return result['IdPasserelle']
    return None




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
    """
    Supprime un client spécifique en fonction de son identifiant
    ainsi que toutes les passerelles associées.
    """
    # Supprimer les passerelles associées
    passerelles = get_passerelle_client_by_client(id_client)
    for passerelle in passerelles:
        delete_passerelle_client(passerelle["IdPasserelle"], id_client)

    # Supprimer le client
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

def get_champ_by_passerelle(passerelle_id):
    """Récupère tous les champs associés à une passerelle spécifique."""
    query = "SELECT * FROM CHAMPS WHERE IdPasserelle = ?"
    return execute_query(query, (passerelle_id, ))

def get_champ_by_logiciel(logiciel_id):
    """Récupère tous les champs associés à un logiciel spécifique."""
    query = "SELECT * FROM CHAMPS WHERE IdLogiciel = ?"
    return execute_query(query, (logiciel_id, ))

def get_champ_by_passerelle_and_logiciel_passerelle(passerelle_id):
    """Récupère tous les champs associés à une passerelle spécifique et à un logiciel passerelle."""
    logiciels = get_logiciels_by_passerelles([passerelle_id])
    if not logiciels:
        return []

    logiciels_ids = [l["IdLogiciel"] for l in logiciels]
    champs_logiciels = get_champs_by_logiciels(logiciels_ids)
    champs_passerelles = get_champs_by_passerelles([passerelle_id])

    return champs_logiciels + champs_passerelles




def add_champ(lib_champ, nom_table, type_champ, id_passerelle=None, id_logiciel=None):
    """Ajoute un champ avec le libellé, le nom de table et le type spécifiés."""
    columns = ["LibChamp", "NomTable", "TypeChamp"]
    values = [lib_champ, nom_table, type_champ]

    if id_passerelle:
        columns.append("IdPasserelle")
        values.append(id_passerelle)

    if id_logiciel:
        columns.append("IdLogiciel")
        values.append(id_logiciel)

    return add_record("CHAMPS", columns, values)

def add_champ_to_passerelle(lib_champ, nom_table, type_champ, lib_passerelle):
    """Ajoute un champ à une passerelle spécifique."""
    id_passerelle = get_id_passerelle_by_lib_passerelle(lib_passerelle)
    return add_champ(lib_champ, nom_table, type_champ, id_passerelle)


def add_champ_to_logiciel(lib_champ, nom_table, type_champ, lib_logiciel):
    """Ajoute un champ à un logiciel spécifique."""
    id_logiciel = get_id_logiciel_by_lib_logiciel(lib_logiciel)
    return add_champ(lib_champ, nom_table, type_champ, id_logiciel=id_logiciel)


def delete_champ(id_champ):
    """Supprime un champ spécifique en fonction de son identifiant."""
    return delete_record("CHAMPS", "IdChamp = ?", (id_champ, ))


def get_lib_champ_by_id(id_champ):
    """Récupère le libellé d'un champ spécifique en fonction de son identifiant."""
    query = "SELECT LibChamp FROM CHAMPS WHERE IdChamp = ?"
    return execute_query_single(query, (id_champ, ))["LibChamp"]



def get_passerelles_by_client(id_client):
    """
    Récupère toutes les passerelles associées à un client spécifique.
    """
    query = """
        SELECT IdPasserelle
        FROM PASSERELLE_CLIENT
        WHERE IdClient = ?
    """
    return execute_query(query, (id_client, ))

def get_logiciels_by_passerelles(passerelles_ids):
    """
    Récupère tous les logiciels associés à des passerelles spécifiques.
    """
    if not passerelles_ids:
        return []

    if isinstance(passerelles_ids, int):
        passerelles_ids = [passerelles_ids]

    query = """
        SELECT DISTINCT L.IdLogiciel, L.LibLogiciel
        FROM CONNECT_LOGICIEL CL
        JOIN LOGICIEL L ON CL.IdLogiciel = L.IdLogiciel
        WHERE CL.IdPasserelle IN ({})
    """.format(','.join('?' for _ in passerelles_ids))

    print(f"Requête SQL pour get_logiciels_by_passerelles : {query}")  # Debug
    print(f"Paramètres pour get_logiciels_by_passerelles : {passerelles_ids}")  # Debug

    results = execute_query(query, passerelles_ids)
    print(f"Résultats de get_logiciels_by_passerelles : {results}")  # Debug
    return results


def get_champs_by_passerelles(passerelles_ids):
    """
    Récupère tous les champs requis pour des passerelles spécifiques.
    """
    query = """
        SELECT CH.*
        FROM CHAMPS CH
        WHERE CH.IdPasserelle IN ({})
    """.format(','.join('?' for _ in passerelles_ids))
    return execute_query(query, passerelles_ids)

def get_champs_by_logiciels(logiciels_ids):
    """
    Récupère tous les champs requis pour des logiciels spécifiques.
    """
    if not logiciels_ids:
        return []

    if isinstance(logiciels_ids, int):
        logiciels_ids = [logiciels_ids]

    query = """
        SELECT CH.*
        FROM CHAMPS CH
        WHERE CH.IdLogiciel IN ({})
    """.format(','.join('?' for _ in logiciels_ids))
    return execute_query(query, logiciels_ids)




def get_all_champs_for_passerelle_client(id_passerelle_client):
    """
    Récupère tous les champs requis pour une passerelle client spécifique.
    """
    query = """
        SELECT CP.*, CH.LibChamp
        FROM CHAMP_PASSERELLE CP
        JOIN CHAMPS CH ON CP.IdChamp = CH.IdChamp
        WHERE CP.IdPasserelleClient = ?
    """
    return execute_query(query, (id_passerelle_client, ))

def get_all_champs_for_client(id_client):
    """
    Récupère tous les champs requis pour un client spécifique.
    """
    # Étape 1: Récupérer les ID des passerelles liées au client
    passerelles = get_passerelles_by_client(id_client)
    passerelles_ids = [p["IdPasserelle"] for p in passerelles]

    if not passerelles_ids:
        return []

    print("liste des passerelles: ", passerelles_ids)

    # Étape 2: Récupérer les logiciels liés à ces passerelles
    logiciels = get_logiciels_by_passerelles(passerelles_ids)
    logiciels_ids = [l["IdLogiciel"] for l in logiciels]

    # Étape 3: Récupérer les champs requis pour les logiciels
    champs_logiciels = get_champs_by_logiciels(logiciels_ids)

    # Étape 4: Récupérer les champs requis pour les passerelles
    champs_passerelles = get_champs_by_passerelles(passerelles_ids)

    # Combiner les résultats des champs
    all_champs = champs_logiciels + champs_passerelles

    return all_champs



def update_date_synchronisation_passerelle_client(id_passerelle_client):
    """
    Met à jour la date de synchronisation d'une passerelle
    client spécifique sous la forme "YYYY-MM-DD".
    """
    query = "UPDATE PASSERELLE_CLIENT SET DateDerSynchronisation = ? WHERE IdPasserelleClient = ?"
    return execute_query(
        query,
        (datetime.datetime.now().strftime("%Y-%m-%d"),
         id_passerelle_client))






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
    return add_record("CONNECT_LOGICIEL",
                      ["IdLogiciel",
                       "IdPasserelle",
                       "IsSource"],
                      [id_logiciel,
                       id_passerelle,
                       is_source])

def delete_connecteur(id_logiciel, id_passerelle):
    """Supprime un connecteur spécifique en fonction de son identifiant."""
    return delete_record("CONNECT_LOGICIEL",
                         "IdLogiciel = ? AND IdPasserelle = ?",
                         (id_logiciel,
                          id_passerelle))

##########################################################################################
#                               CHAMP_PASSERELLE                                        #
##########################################################################################

def add_champ_passerelle(id_passerelle_client, id_champ, valeur):
    """Ajoute un champ passerelle avec l'identifiant, la valeur et IdChamp spécifiés."""
    return add_record("CHAMP_PASSERELLE",
                      ["IdChamp",
                       "IdPasserelleClient",
                       "Valeur"],
                      [id_champ, id_passerelle_client, valeur])





def get_all_champ_passerelle_by_passerelle_client(id_passerelle_client):
    """Récupère tous les champs passerelle associés à une passerelle client spécifique."""
    query = "SELECT * FROM CHAMP_PASSERELLE WHERE IdPasserelleClient = ?"
    return execute_query(query, (id_passerelle_client, ))

def get_all_champ_passerelle_by_passerelle_client_with_lib_champ(id_passerelle_client):
    """
    Récupère tous les champs passerelle associés à une
    passerelle client spécifique avec le libellé du champ.
    """
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
    """
    Récupère un champ passerelle spécifique en fonction du libellé
    du champ et de l'identifiant de la passerelle client.
    """
    query = """
        SELECT CP.*
        FROM CHAMP_PASSERELLE CP
        JOIN CHAMPS CH ON CP.IdChamp = CH.IdChamp
        WHERE CP.IdPasserelleClient = ? AND CH.LibChamp = ?
    """
    return execute_query_single(query, (id_passerelle_client, lib_champ))


def delete_champ_passerelle(id_champ, id_passerelle_client):
    """Supprime un champ passerelle spécifique en fonction de son identifiant."""
    return delete_record("CHAMP_PASSERELLE",
                         "IdChamp = ? AND IdPasserelleClient = ?",
                         (id_champ, id_passerelle_client))

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
    """
    Récupère tous les champs passerelle associés
    à un client spécifique avec le libellé du champ.
    """
    query = """
        SELECT CH.*, CP.Valeur, P.LibPasserelle
        FROM CHAMPS CH
        JOIN CHAMP_PASSERELLE CP ON CH.IdChamp = CP.IdChamp
        JOIN PASSERELLE_CLIENT PC ON CP.IdPasserelleClient = PC.IdPasserelleClient
        JOIN PASSERELLE P ON PC.IdPasserelle = P.IdPasserelle
        WHERE PC.IdClient = ?

    """
    return execute_query(query, (id_client, ))


def get_champ_passerelle_client_by_passerelle_with_lib_champ(id_passerelle_client):
    """
    Récupère tous les champs passerelle associés à une passerelle
    client spécifique avec le libellé du champ.
    """
    query = """
        SELECT CH.IdChamp, CH.LibChamp, CP.Valeur
        FROM CHAMPS CH
        JOIN CHAMP_PASSERELLE CP ON CH.IdChamp = CP.IdChamp
        WHERE CP.IdPasserelleClient = ?
    """
    try:
        result = execute_query(query, (id_passerelle_client, ))
        logging.debug(
            "Résultat de la requête pour id_passerelle_client=%s: %s",
            id_passerelle_client, result
        )

        return result
    except Exception as e:
        logging.error(
            "Erreur lors de l'exécution de la requête pour id_passerelle_client=%s: %s",
            id_passerelle_client, e
        )

        return None


def get_champ_passerelle_client_by_ids_with_lib_champ(id_passerelle_client):
    """
    Récupère tous les champs passerelle associés à une
    passerelle client spécifique avec le libellé du champ.
    """
    query = """
        SELECT CH.*, CP.Valeur
        FROM CHAMPS CH
        JOIN CHAMP_PASSERELLE CP ON CH.IdChamp = CP.IdChamp
        WHERE CP.IdPasserelleClient = ?
    """
    return execute_query(query, (id_passerelle_client,))






def get_champ_passerelle_required_by_passerelle_client(id_passerelle_client):
    """Récupère tous les champs passerelle requis associés à une passerelle client spécifique."""
    # Etape 2: recuperer l'id de la passerelle
    passerelle = get_passerelle_client_by_id(id_passerelle_client)
    id = passerelle["IdPasserelle"]

    # Etape 3: recuperer les logiciels associés à la passerelle
    logiciels = get_logiciels_by_passerelles([id])


    # Etape 4: recuperer les champs requis pour les logiciels
    champs_logiciels = get_champs_by_logiciels([l["IdLogiciel"] for l in logiciels])

    # Etape 5: recuperer les champs requis pour la passerelle
    champs_passerelles = get_champs_by_passerelles([id])

    # Combiner les résultats des champs
    all_champs = champs_logiciels + champs_passerelles

    return all_champs




def add_multiple_champ_passerelle(id_passerelle_client, champs, id_client):   # pylint: disable=too-many-arguments
    """Ajoute plusieurs champs passerelle à un client spécifique."""
    for champ in champs:
        print("Champ à ajouter: ", champ)

        add_or_update_champ_passerelle(id_passerelle_client, [champ])



def add_or_update_champ_passerelle(id_passerelle_client, champs):
    """
    Ajoute ou met à jour plusieurs champs passerelle pour un client spécifique.
    """
    for champ in champs:
        if champ["Valeur"] == "":
            continue

        champ_passerelle = get_champ_passerelle_by_id(champ["id_champ"], id_passerelle_client)
        if champ_passerelle:
            query = """
            UPDATE CHAMP_PASSERELLE
            SET Valeur = ?
            WHERE IdChamp = ?
            AND IdPasserelleClient = ?"""
            execute_query(query, (champ["Valeur"], champ["id_champ"], id_passerelle_client))
        else:
            add_champ_passerelle(id_passerelle_client, champ["id_champ"], champ["Valeur"])




def get_or_create_passerelle_client(id_passerelle, id_client):
    """
    Récupère ou crée une entrée dans la table PASSERELLE_CLIENT.
    """
    logging.debug(
        "get_or_create_passerelle_client called with id_passerelle: %s, id_client: %s",
        id_passerelle, id_client
    )

    passerelle_client = get_passerelle_client_by_ids(id_passerelle, id_client)
    if passerelle_client:
        logging.debug(f"Passerelle client found: {passerelle_client}")
        return passerelle_client["IdPasserelleClient"]

    id_passerelle_client = add_passerelle_client(id_passerelle, id_client)
    logging.debug(f"New passerelle client created with id: {id_passerelle_client}")
    return id_passerelle_client










##########################################################################################
#                               PASSERELLE_CLIENT                                       #
##########################################################################################

def add_passerelle_client(id_passerelle, id_client):
    """Ajoute une entrée dans la table PASSERELLE_CLIENT et retourne l'ID généré."""
    logging.debug(
        f"add_passerelle_client called with id_passerelle: {id_passerelle}, id_client: {id_client}")
    add_record("PASSERELLE_CLIENT", ["IdPasserelle", "IdClient"], [id_passerelle, id_client])
    query = """
    SELECT IdPasserelleClient
    FROM PASSERELLE_CLIENT
    WHERE IdPasserelle = ?
    AND IdClient = ?
    """
    result = execute_query_single(query, (id_passerelle, id_client))
    logging.debug(f"Result from add_passerelle_client: {result}")
    return result["IdPasserelleClient"] if result else None








def get_all_passerelle_client():
    """Récupère toutes les entrées de la table PASSERELLE_CLIENT."""
    return get_all_records("PASSERELLE_CLIENT")

def get_all_passerelle_client_with_lib_passerelle():
    """
    Récupère toutes les entrées de la table PASSERELLE_CLIENT
    avec le libellé de la passerelle.
    """
    query = """
        SELECT pc.*, p.LibPasserelle
        FROM PASSERELLE_CLIENT pc
        JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
    """
    return execute_query(query)

def get_passerelle_client_by_id(id_passerelle_client):
    """Récupère une entrée spécifique de la table PASSERELLE_CLIENT."""
    return get_record_by_id("PASSERELLE_CLIENT", "IdPasserelleClient", id_passerelle_client)

def get_passerelle_client_by_ids(id_passerelle, id_client):
    """
    Récupère une entrée spécifique de la table PASSERELLE_CLIENT.
    """
    logging.debug(
        "get_passerelle_client_by_ids called with id_passerelle: %s, id_client: %s",
        id_passerelle, id_client
    )

    query = "SELECT * FROM PASSERELLE_CLIENT WHERE IdPasserelle = ? AND IdClient = ?"
    result = execute_query_single(query, (id_passerelle, id_client))
    logging.debug(f"Result from get_passerelle_client_by_ids: {result}")
    return result


def get_date_synchronisation_passerelle_client(id_passerelle_client):
    """
    Récupère la date de synchronisation d'une passerelle client spécifique
    sous la forme "YYYY-MM-DD".
    """
    query = "SELECT DateDerSynchronisation FROM PASSERELLE_CLIENT WHERE IdPasserelleClient = ?"
    return execute_query_single(query, (id_passerelle_client, ))["DateDerSynchronisation"]



def get_passerelle_client_by_client(id_client):
    """Récupère toutes les passerelles associées à un client spécifique."""
    query = "SELECT * FROM PASSERELLE_CLIENT WHERE IdClient = ?"
    return execute_query(query, (id_client, ))

def get_passerelle_client_with_lib_passerelle(id_client):
    """
    Récupère toutes les passerelles associées à un client
    spécifique avec le libellé de la passerelle.
    """
    query = """
        SELECT pc.*, p.LibPasserelle
        FROM PASSERELLE_CLIENT pc
        JOIN PASSERELLE p ON pc.IdPasserelle = p.IdPasserelle
        WHERE pc.IdClient = ?
    """
    return execute_query(query, (id_client, ))

def delete_passerelle_client(id_passerelle, id_client):
    """
    Supprime une entrée spécifique de la table PASSERELLE_CLIENT
    ainsi que tous les champs passerelle associés.
    """
    # Supprimer les champs passerelle associés
    champs = get_all_champ_passerelle_by_passerelle_client(get_passerelle_client_by_ids(
        id_passerelle,
        id_client)["IdPasserelleClient"])

    for champ in champs:
        delete_champ_passerelle(champ["IdChamp"], champ["IdPasserelleClient"])

    # Supprimer l'entrée PASSERELLE_CLIENT
    return delete_record(
        "PASSERELLE_CLIENT",
        "IdPasserelle = ? AND IdClient = ?",
        (id_passerelle, id_client))


def add_passerelle_logiciel(id_passerelle, id_logiciel):
    """Ajoute une entrée dans la table CONNECT_LOGICIEL."""
    return add_record(
        "CONNECT_LOGICIEL",
        ["IdPasserelle", "IdLogiciel"],
        [id_passerelle, id_logiciel])




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
