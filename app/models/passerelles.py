
import datetime
import json

from app.models.ebp import EBP
from app.models.zeendoc import Zeendoc
from app.models import database


def routine():
    # on récupère la liste passerelles
    passerelles = database.get_all_passerelle_client_with_lib_passerelle()


    for passerelle in passerelles:
        # on récupère l'id de la passerelle
        IdPasserelleClient = passerelle['IdPasserelleClient']

        if passerelle['LibPasserelle'] == "remontée de paiement":
            P_remonte_paiement(IdPasserelleClient)


    return "Routine terminée avec succès."




def P_remonte_paiement(IdPasserelleClient):
    """
    Fonction pour la passerelle remontée de paiement.
    """

    print("P_remonte_paiement - IdPasserelleClient: ", IdPasserelleClient)

    datas = database.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(IdPasserelleClient)

    # connexion à EBP
    ebp = EBP(IdPasserelleClient)
    ebp.login()


    # connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    # recupération de l'index de paiement
    indexPaiement = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "INDEX_STATUT_PAIEMENT")
    indexPaiement = indexPaiement['Valeur']
    # on récupère les documents payés dans EBP
    paiddoc = ebp.get_paid_documents()


    paiddoc = json.loads(paiddoc)



    for doc in paiddoc['results']:
        # on récupère le numéro de document
        document_number = doc['DocumentNumber']

        print("document_number: ", document_number)

        print("indexPaiement: ", indexPaiement)

        # on modifie le document dans zeendoc
        res = zeendoc.update_doc_paiement_by_ref(ref=document_number, index=indexPaiement)

        print("res: ", res)









