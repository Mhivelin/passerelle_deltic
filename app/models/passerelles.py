"""
Ce module contient les fonctions de routine pour les passerelles.
"""

import datetime
import json
import logging

from app.models import database  # pylint: disable=E0401
from app.models.ebp import EBP  # pylint: disable=E0401
from app.models.sellsy import Sellsy  # pylint: disable=E0401
from app.models.zeendoc import Zeendoc  # pylint: disable=E0401

# Configuration du logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def routine():
    """
    Routine qui traite les passerelles une par une.
    """
    # on récupère la liste passerelles
    passerelles = database.get_all_passerelle_client_with_lib_passerelle()
    logger.info(
        "Routine démarrée. Nombre de passerelles à traiter: %d", len(passerelles)
    )

    for passerelle in passerelles:
        # on récupère l'id de la passerelle
        id_passerelle_client = passerelle["IdPasserelleClient"]

        try:
            if (
                passerelle["LibPasserelle"]
                == "remontée de paiement date EBP --> Zeendoc"
            ):
                value = datetime.datetime.now().strftime("%Y-%m-%d")
                p_remonte_paiement_ebp_zeendoc(id_passerelle_client, value)
            elif (
                passerelle["LibPasserelle"] == "remontée de fournisseur EBP --> Zeendoc"
            ):
                p_remonte_fournisseur(id_passerelle_client)
            elif (
                passerelle["LibPasserelle"]
                == "remontée de paiement statut EBP --> Zeendoc"
            ):
                p_remonte_paiement_ebp_zeendoc(id_passerelle_client, "1")
            elif (
                passerelle["LibPasserelle"]
                == "remontée de paiement date Sellsy --> Zeendoc"
            ):
                p_remonte_paiement_sellsy_zeendoc(id_passerelle_client)
            else:
                logger.info("Passerelle non reconnue: %s", passerelle["LibPasserelle"])
                continue

            logger.info(
                "mise à jour de la date de synchronisation de la passerelle: %d",
                passerelle["IdPasserelleClient"],
            )
            database.update_date_synchronisation_passerelle_client(
                passerelle["IdPasserelleClient"]
            )

        except KeyError as e:
            logger.error(
                "Clé non trouvée lors du traitement de la passerelle %d: %s",
                id_passerelle_client,
                e,
            )
        except ValueError as e:
            logger.error(
                "Valeur incorrecte lors du traitement de la passerelle %d: %s",
                id_passerelle_client,
                e,
            )
        except TypeError as e:
            logger.error(
                "Type incorrect lors du traitement de la passerelle %d: %s",
                id_passerelle_client,
                e,
            )
        except Exception as e:  # pylint: disable=W0703
            logger.error(
                "Erreur inattendue lors du traitement de la passerelle %d: %s",
                id_passerelle_client,
                e,
            )

    logger.info("Routine terminée avec succès.")
    return "Routine terminée avec succès."


def p_remonte_paiement_ebp_zeendoc(IdPasserelleClient, value):  # pylint: disable=C0103
    """
    Fonction pour la passerelle remontée de paiement.
    """
    logger.info(
        "p_remonte_paiement_ebp_zeendoc - IdPasserelleClient: %d", IdPasserelleClient
    )

    # datas = database.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(
    #     IdPasserelleClient)

    # connexion à EBP
    ebp = EBP(IdPasserelleClient)
    ebp.login()

    # connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    # recupération de l'index de paiement
    index_paiement = database.get_champ_passerelle_by_lib_champ(
        IdPasserelleClient, "INDEX_STATUT_PAIEMENT"
    )
    index_paiement = index_paiement["Valeur"]
    # on récupère les documents payés dans EBP
    paiddoc = ebp.get_paid_documents()
    paiddoc = json.loads(paiddoc)

    for doc in paiddoc["results"]:
        # on récupère le numéro de document
        document_number = doc["DocumentNumber"]
        logger.info("document_number: %s", document_number)
        logger.info("index_paiement: %s", index_paiement)

        # on modifie le document dans zeendoc
        res = zeendoc.update_doc_paiement_by_ref(
            ref=document_number, index=index_paiement, value=value
        )
        logger.info("res: %s", res)
        print("res: ", res)


def p_remonte_fournisseur(IdPasserelleClient):  # pylint: disable=C0103
    """
    Fonction pour la passerelle remontée de fournisseur.
    """
    logger.info("p_remonte_fournisseur - IdPasserelleClient: %d", IdPasserelleClient)

    # Extraction correcte des valeurs de coll_id et column_name
    coll_id_data = database.get_champ_passerelle_by_lib_champ(
        IdPasserelleClient, "Zeendoc_CLASSEUR"
    )
    column_name_data = database.get_champ_passerelle_by_lib_champ(
        IdPasserelleClient, "INDEX_FOURNISSEUR"
    )

    coll_id = coll_id_data["Valeur"]
    column_name = column_name_data["Valeur"]

    # Connexion à EBP
    ebp = EBP(IdPasserelleClient)
    ebp.login()

    # Connexion à Zeendoc
    zeendoc = Zeendoc(IdPasserelleClient)

    # Récupération de la liste des fournisseurs
    suppliers = ebp.get_suppliers()
    suppliers = json.loads(suppliers)

    for supplier in suppliers["results"]:
        # concatener le nom et le compte du fournisseur sous
        # la forme : 401FOURN - NOM DU FOURNISSEUR
        supplier["name"] = f"{supplier['Accounts_Account']} - {supplier['name']}"

    items = [supplier["name"] for supplier in suppliers["results"]]

    # Récupérer les fournisseurs deja existants dans la liste déroulante
    existing_items = zeendoc.get_items_list(coll_id, column_name)
    existing_items = [item["Label"] for item in existing_items]

    # Ajouter les fournisseurs qui ne sont pas déjà dans la liste déroulante
    items = list(set(items) - set(existing_items))

    # Ajouter les fournisseurs à la liste déroulante dans Zeendoc
    response = zeendoc.add_items_list(coll_id, column_name, items)

    if response and response.get("Result") == 0:
        logger.info("Ajout des fournisseurs réussi.")
    else:
        logger.error("Erreur lors de l'ajout des fournisseurs: %s", response)

    return response


def p_remonte_paiement_sellsy_zeendoc(IdPasserelleClient):
    logger.info("p_remonte_paiement_sellsy_zeendoc - IdPasserelleClient: %d", IdPasserelleClient)

    sellsy = Sellsy(IdPasserelleClient)
    zeendoc = Zeendoc(IdPasserelleClient)
    paiddoc = sellsy.get_paid_invoices_with_last_payment()

    if not paiddoc:
        logger.error("No paid invoices found")
        return

    index = database.get_champ_passerelle_by_lib_champ(
        IdPasserelleClient, "INDEX_STATUT_PAIEMENT"
    )["Valeur"]

    for doc in paiddoc:
        logger.info(f"Processing document: {doc}")
        # 2024-07-18 09:01:14,123 - INFO - Processing document: {'id': 13122621, 'date': '2019-05-20', 'created': '2019-05-20T11:46:11+02:00', 'related': [{'type': 'company', 'id': 5783612}, {'type': 'contact', 'id': 4209872}], 'number': 'F-1905-129', 'amounts': {'total_raw_excl_tax': '2100.000', 'total_after_discount_excl_tax': '2100.000', 'total_packaging': '0.000', 'total_shipping': '0.000', 'total_excl_tax': '2100.000', 'total_incl_tax': '2520.000', 'total_remaining_due_incl_tax': '0.000', 'total_primes_incl_tax': '0.000'}, 'currency': 'EUR', 'public_link': {'enabled': False, 'url': 'https://sellsy.link/kKbjMv2'}, 'pdf_link': 'https://file.sellsy.com/?id=JUE0JTdDJTlBMkNsJTg2ZCUzQiVGQSUwNTglNUIlQkMlQjYlQTUlOEMlQjYlMTAlMDElQzYlRDIlQjklM0UzJTAwJTdEUVpMViVGMSVBNiUxQSUxMEYlQjklQjklN0UlQzQlMDElODQlODVnJUZEJTlBJTE4JTA4JTAzJTgwJUFGKyVEQSVFMSU5MSVFMCUwOSVCMSVDQUElMTUlODQlREMlOUIlRjAlRUYlMDMlRDhaJUU5TSUyNCUwRSUxQkQlRDclN0MlQUIlOEYlMTYlQkMlRDElODUlRUZEJUEzViVDNiVGOCVDRSUxRStMJUI2JUU2JUMxJUUwJUE0JTI2WCVBRGQlMDNCJTNEJUE1JTVCJTkyTCVDMlVNNyUyQiUwQyVFQyVCMSVCRiUwMSUxMUclMDNNJUEzbyVENCVGMiVBRg==&key=007ea9fc54fa11fe42464c344b6cfbbc&display=Y', 'taxes': [{'label': 'TVA 20%', 'id': 2016322, 'rate': '20.000000000', 'amount': '420.000'}], 'discount': None, 'owner': {'id': 69391, 'type': 'staff'}, 'fiscal_year_id': 18934, 'subject': 'Client Music Global Consulting', 'assigned_staff_id': 69391, 'invoicing_address_id': 59062477, 'delivery_address_id': 59062478, 'decimal_number': {'main': 3, 'quantity': 3, 'unit_price': 3}, 'contact_id': 4209872, 'rate_category_id': 85028, 'service_dates': None, 'note': 'Maintenance annuelle à échoir 387€HT/an<br /><div style="text-align:justify;">sur la durée du contrat : 60 mois</div>', 'status': 'paid', 'payment_conditions_acceptance': {'enabled': False}, 'is_deposit': False, 'due_date': '2019-06-30', 'parent': {'type': 'estimate', 'id': 12541243}, 'order_reference': '', 'subscription_id': None, 'is_sent_to_accounting': False, 'shipping_date': None, 'last_payment': {'id': 7841596, 'number': None, 'paid_at': '2019-11-07T10:55:57+01:00', 'status': 'confirmed', 'payment_method_id': 2016308, 'type': 'credit', 'amount': {'value': '2520.00', 'currency': 'EUR'}, 'related': [{'type': 'invoice', 'id': 13122621}]}}

        try:
            last_payment = doc.get("last_payment")
            if not last_payment:
                raise Exception(f"No payments found for document: {doc['number']}")
            else:
                paid_at = last_payment["paid_at"].split("T")[0]

            res = zeendoc.update_doc_paiement_by_num_facture(doc["number"], index, paid_at)
            logger.info(f"Updated document in Zeendoc: {doc['number']} with response: {res}")

            # Update the document in Sellsy
            res = sellsy.update_invoice_smart_tags(doc["id"], [{"value": "paiement exporté"}])
            logger.info(f"Updated smart tags in Sellsy for document: {doc['number']} with response: {res}")

        except KeyError as e:
            logger.error(f"Clé non trouvée lors du traitement de la passerelle {IdPasserelleClient}: {e}")
            res = sellsy.update_invoice_smart_tags(doc["id"], [{"value": "erreur export"}])

        except Exception as e:
            logger.error(f"Erreur inattendue lors du traitement de la passerelle {IdPasserelleClient}: {e}")
            res = sellsy.update_invoice_smart_tags(doc["id"], [{"value": "erreur export"}])



    logger.info("Routine terminée avec succès.")







