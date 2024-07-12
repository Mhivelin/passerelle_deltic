"""
Ce fichier contient la connexion à la base de données.
"""

import sqlite3


def get_db_connection():
    """
    Fonction pour la connexion à la base de données.
    """
    conn = sqlite3.connect("BDPasserelle.db")
    conn.row_factory = sqlite3.Row
    return conn
