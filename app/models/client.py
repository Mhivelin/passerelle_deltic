"""
Ce module contient la classe Client.
"""

# import json

from app.models.ebp import EBP  # pylint: disable=E0401
from app.models.zeendoc import Zeendoc  # pylint: disable=E0401

# from app.models.database import get_db_connection


class Client:
    """
    Represents a client.

    Attributes:
        id (int): The client's ID.
        username (str): The client's username.
        lastUpdate (str): The last update timestamp.
        clientZeendoc (Zeendoc): The Zeendoc client instance.
        clientEBP (EBP): The EBP client instance.
    """

    def __init__(self, id) -> None:

        self.id = id

        res = self.BdGetClient()

        self.username = res["username"]  # pylint: disable=E1101
        idclientZeendoc = res["id_1"]  # pylint: disable=E1101
        idclientEBP = res["id_2"]  # pylint: disable=E1101
        self.lastUpdate = res["LastUpdate"]  # pylint: disable=E1101

        self.clientZeendoc = Zeendoc(idclientZeendoc)
        self.clientEBP = EBP(idclientEBP)
