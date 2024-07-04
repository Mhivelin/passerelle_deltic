
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

        if passerelle['LibPasserelle'] == "remontée de paiement date EBP --> Zeendoc":
            value = datetime.datetime.now().strftime("%Y-%m-%d")
            P_remonte_paiement(IdPasserelleClient, value)
        if passerelle['LibPasserelle'] == "remontée de fournisseur EBP --> Zeendoc":
            P_remonte_fournisseur(IdPasserelleClient)
        if passerelle['LibPasserelle'] == "remontée de paiement statut EBP --> Zeendoc":
            P_remonte_paiement(IdPasserelleClient, "1")


        print("mise à jour de la date de synchronisation de la passerelle: ", passerelle['IdPasserelleClient'])
        database.update_date_synchronisation_passerelle_client(passerelle['IdPasserelleClient'])


    return "Routine terminée avec succès."




def P_remonte_paiement(IdPasserelleClient, value):
    """
    Fonction pour la passerelle remontée de paiement.
    """

    # print("P_remonte_paiement - IdPasserelleClient: ", IdPasserelleClient)

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
        res = zeendoc.update_doc_paiement_by_ref(ref=document_number, index=indexPaiement, value=value)

        print("res: ", res)



def P_remonte_fournisseur(IdPasserelleClient):
    """
    Fonction pour la passerelle remontée de fournisseur.
    """

    print("P_remonte_fournisseur - IdPasserelleClient: ", IdPasserelleClient)

    # Extraction correcte des valeurs de coll_id et column_name
    coll_id_data = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "Zeendoc_CLASSEUR")
    column_name_data = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "INDEX_FOURNISSEUR")

    coll_id = coll_id_data['Valeur']
    column_name = column_name_data['Valeur']

    # Connexion à EBP
    ebp = EBP(IdPasserelleClient)
    ebp.login()

    # Connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    # Récupération de la liste des fournisseurs
    suppliers = ebp.get_suppliers()
    suppliers = json.loads(suppliers)

    print("suppliers: ", suppliers)
    # suppliers:  {'results': [{'name': 'lana', 'Id': 'FR00001', "Accounts_Account": "401FR00001"}], 'paging': {'total': 1, 'returned': 1, 'offset': 0, 'limit': 500}}

    for supplier in suppliers['results']:
        # concatener le nom et le compte du fournisseur sous la forme : 401FOURN - NOM DU FOURNISSEUR
        supplier['name'] = f"{supplier['Accounts_Account']} - {supplier['name']}"


    items = [supplier['name'] for supplier in suppliers['results']]





    # Récupérer les fournisseurs deja existants dans la liste déroulante
    existing_items = zeendoc.get_items_list(coll_id, column_name)

    # [{'Id': '17', 'Label': 'lana'}]

    existing_items = [item['Label'] for item in existing_items]

    # Ajouter les fournisseurs qui ne sont pas déjà dans la liste déroulante
    items = list(set(items) - set(existing_items))





    # Ajouter les fournisseurs à la liste déroulante dans Zeendoc
    response = zeendoc.add_items_list(coll_id, column_name, items)

    if response and response.get('Result') == 0:
        print("Ajout des fournisseurs réussi.")
    else:
        print(f"Erreur lors de l'ajout des fournisseurs: {response}")

    return response



