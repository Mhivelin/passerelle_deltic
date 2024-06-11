
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

    print("Datas: ", datas)
    # connexion à EBP
    ebp = EBP(IdPasserelleClient)
    ebp.login()

    print("EBP login success")

    # connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    # on récupère les documents payés dans EBP
    paiddoc = ebp.get_paid_documents()

    print(paiddoc)

    paiddoc = json.loads(paiddoc)

    output_index = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "OUTPUT_INDEX")['Valeur']

    # print(output_index)


    # print(zeendoc.getAllDoc())

    for doc in paiddoc['results']:
        # on récupère le numéro de document
        document_number = doc[output_index]


        # on vérifie si le document existe dans zeendoc
        if zeendoc.GetDocRef(document_number) == 0:
            # on recupère l'index a modifier
            index = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "INPUT_INDEX")['Valeur']

            # on passe l'index a payé
            zeendoc.SetDocRef(document_number, index)







