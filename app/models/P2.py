import datetime
import json
import sys

from app.models.database import get_db_connection
from app.models.ebp import EBP
from app.models.zeendoc import Zeendoc


class Client:

    def __init__(self, id) -> None:

        self.id = id

        res = self.BdGetClient(id)

        self.username = res["username"]
        idclientZeendoc = res["id_1"]
        idclientEBP = res["id_2"]
        self.lastUpdate = res["LastUpdate"]

        self.clientZeendoc = Zeendoc(idclientZeendoc)
        self.clientEBP = EBP(idclientEBP)

    def getModelBD(self):
        conn = get_db_connection()

        champs = {"Nom": "username"}

        self.clientEBP.getModelBD()

    def BdGetClient(self, id):

        conn = get_db_connection()

        try:
            client = conn.execute("SELECT * FROM CLIENT WHERE id = ?",
                                  (self.id, )).fetchone()
            return dict(client)
        except:
            return None
        finally:
            conn.close()

    def setLastUpdatenow(self):

        conn = get_db_connection()

        try:
            # date sous la forme 1999-01-01T10:00:10+02:00

            date = datetime.datetime.now().isoformat(timespec="seconds")

            print(date)
            conn.execute("UPDATE CLIENT SET LastUpdate = ? WHERE id = ?",
                         (date, self.id))
            conn.commit()
        except:
            print("erreur lors de la mise à jour de la date : ")
            print(sys.exc_info()[0])
        finally:
            conn.close()

    def routine(self):

        try:
            docEBP = self.clientEBP.getPaidPurchaseDocument(
                self.clientEBP.ebp_folder_id, self.lastUpdate)
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

    def update_client(
        self,
        username,
        LastUpdate,
        EBP_CLIENT_ID,
        EBP_CLIENT_SECRET,
        EBP_SUBSCRIPTION_KEY,
        EBP_FOLDER_ID,
        ZEENDOC_LOGIN,
        ZEENDOC_URLCLIENT,
        ZEENDOC_CLASSEUR,
        ZEENDOC_CPASSWORD,
    ):

        conn = get_db_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                UPDATE CLIENT
                SET username = ?, LastUpdate = ?
                WHERE id = ?""",
                (username, LastUpdate, self.id),
            )

            cur.execute(
                """
                UPDATE CLIENT_EBP
                SET EBP_CLIENT_ID = ?, EBP_CLIENT_SECRET = ?, EBP_SUBSCRIPTION_KEY = ?, EBP_FOLDER_ID = ?
                WHERE id = ?""",
                (
                    EBP_CLIENT_ID,
                    EBP_CLIENT_SECRET,
                    EBP_SUBSCRIPTION_KEY,
                    EBP_FOLDER_ID,
                    self.id,
                ),
            )

            cur.execute(
                """
                UPDATE CLIENT_ZEENDOC
                SET ZEENDOC_LOGIN = ?, ZEENDOC_URLCLIENT = ?, ZEENDOC_CLASSEUR = ?, ZEENDOC_CPASSWORD = ?
                WHERE id = ?""",
                (
                    ZEENDOC_LOGIN,
                    ZEENDOC_URLCLIENT,
                    ZEENDOC_CLASSEUR,
                    ZEENDOC_CPASSWORD,
                    self.id,
                ),
            )

            conn.commit()
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la base de données: {e}")
        finally:
            conn.close()
