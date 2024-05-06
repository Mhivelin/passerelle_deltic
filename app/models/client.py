import datetime
import json
import sys

from app.models.ebp import EBP
from app.models.zeendoc import Zeendoc

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

        self.username = res["username"]
        idclientZeendoc = res["id_1"]
        idclientEBP = res["id_2"]
        self.lastUpdate = res["LastUpdate"]

        self.clientZeendoc = Zeendoc(idclientZeendoc)
        self.clientEBP = EBP(idclientEBP)

    def routine(self):
        try:
            docEBP = self.clientEBP.getPaidPurchaseDocument(
                self.clientEBP.ebp_folder_id, "1999-01-01")
            print("docEBP : ", docEBP)
            docEBP = json.loads(docEBP)
        except Exception as e:
            print(
                f"Erreur lors de la récupération ou de la conversion des documents EBP: {e}"
            )
            return  # ou continue, selon la logique souhaitée

        for doc in docEBP.get("results", []):
            try:
                docZeendoc = self.clientZeendoc.GetDocRef(
                    doc["DocumentNumber"])
                self.clientZeendoc.updateDocPaiement(
                    docZeendoc["Document"][0]["Res_Id"])
                print(
                    f"Le doc {docZeendoc['Document'][0]['Res_Id']} a été mis à jour"
                )
            except Exception as e:
                print(f"Erreur lors de la mise à jour d'un document: {e}")

        self.setLastUpdatenow()
