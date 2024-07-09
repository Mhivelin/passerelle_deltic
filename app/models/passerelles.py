import datetime
import json
import logging

from app.models.ebp import EBP
from app.models.zeendoc import Zeendoc
from app.models.sellsy import Sellsy
from app.models import database

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def routine():
    # on récupère la liste passerelles
    passerelles = database.get_all_passerelle_client_with_lib_passerelle()
    logger.info("Routine démarrée. Nombre de passerelles à traiter: %d", len(passerelles))

    for passerelle in passerelles:
        # on récupère l'id de la passerelle
        IdPasserelleClient = passerelle['IdPasserelleClient']

        try:

            if passerelle['LibPasserelle'] == "remontée de paiement date EBP --> Zeendoc":
                value = datetime.datetime.now().strftime("%Y-%m-%d")
                P_remonte_paiement_EBP_Zeendoc(IdPasserelleClient, value)
            elif passerelle['LibPasserelle'] == "remontée de fournisseur EBP --> Zeendoc":
                P_remonte_fournisseur(IdPasserelleClient)
            elif passerelle['LibPasserelle'] == "remontée de paiement statut EBP --> Zeendoc":
                P_remonte_paiement_EBP_Zeendoc(IdPasserelleClient, "1")
            elif passerelle['LibPasserelle'] == "remontée de paiement date Sellsy --> Zeendoc":
                P_remonte_paiement_Sellsy_Zeendoc(IdPasserelleClient)
            else:
                logger.info("Passerelle non reconnue: %s", passerelle['LibPasserelle'])
                continue


            logger.info("mise à jour de la date de synchronisation de la passerelle: %d", passerelle['IdPasserelleClient'])
            database.update_date_synchronisation_passerelle_client(passerelle['IdPasserelleClient'])


        except Exception as e:
            logger.error("Erreur lors du traitement de la passerelle %d: %s", IdPasserelleClient, e)
            continue



    logger.info("Routine terminée avec succès.")
    return "Routine terminée avec succès."


def P_remonte_paiement_EBP_Zeendoc(IdPasserelleClient, value):
    """
    Fonction pour la passerelle remontée de paiement.
    """
    logger.info("P_remonte_paiement_EBP_Zeendoc - IdPasserelleClient: %d", IdPasserelleClient)

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
        logger.info("document_number: %s", document_number)
        logger.info("indexPaiement: %s", indexPaiement)

        # on modifie le document dans zeendoc
        res = zeendoc.update_doc_paiement_by_ref(ref=document_number, index=indexPaiement, value=value)
        logger.info("res: %s", res)


def P_remonte_fournisseur(IdPasserelleClient):
    """
    Fonction pour la passerelle remontée de fournisseur.
    """
    logger.info("P_remonte_fournisseur - IdPasserelleClient: %d", IdPasserelleClient)

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


    for supplier in suppliers['results']:
        # concatener le nom et le compte du fournisseur sous la forme : 401FOURN - NOM DU FOURNISSEUR
        supplier['name'] = f"{supplier['Accounts_Account']} - {supplier['name']}"

    items = [supplier['name'] for supplier in suppliers['results']]

    # Récupérer les fournisseurs deja existants dans la liste déroulante
    existing_items = zeendoc.get_items_list(coll_id, column_name)
    existing_items = [item['Label'] for item in existing_items]

    # Ajouter les fournisseurs qui ne sont pas déjà dans la liste déroulante
    items = list(set(items) - set(existing_items))

    # Ajouter les fournisseurs à la liste déroulante dans Zeendoc
    response = zeendoc.add_items_list(coll_id, column_name, items)

    if response and response.get('Result') == 0:
        logger.info("Ajout des fournisseurs réussi.")
    else:
        logger.error("Erreur lors de l'ajout des fournisseurs: %s", response)

    return response


def P_remonte_paiement_Sellsy_Zeendoc(IdPasserelleClient):
    """
    Fonction pour la passerelle remontée de paiement.
    """
    logger.info("P_remonte_paiement_Sellsy_Zeendoc - IdPasserelleClient: %d", IdPasserelleClient)

    datas = database.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(IdPasserelleClient)

    # connexion à Sellsy
    sellsy = Sellsy(IdPasserelleClient)

    # connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    paiddoc = sellsy.get_paid_invoices_with_last_payment()
    index = database.get_champ_passerelle_by_lib_champ(IdPasserelleClient, "INDEX_STATUT_PAIEMENT")['Valeur']

    for doc in paiddoc:
        paid_at = doc['last_payment']['paid_at']
        paid_at = paid_at.split("T")[0]

        # on modifie le document dans zeendoc
        res = zeendoc.update_doc_paiement_by_num_facture(num_facture=doc['number'], index=index, value=paid_at)
        logger.info("Update response: %s", res)
