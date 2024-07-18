"""
Ce module contient la classe Zeendoc qui permet de gérer les requêtes vers l'API Zeendoc
"""

import json
import xml.etree.ElementTree as ET

import requests

# import sys
import app.models.database as db  # pylint: disable=E0401

# import datetime


class Zeendoc:
    """
    Classe qui permet de gérer les requêtes vers l'API Zeendoc
    """

    def __init__(self, id) -> None:
        """
        Constructeur de la classe Zeendoc
        """
        infos = db.get_all_champ_passerelle_by_passerelle_client_with_lib_champ(id)
        self.log = self._get_info_value(infos, "Zeendoc_Login")
        self.cpassword = self._get_info_value(infos, "Zeendoc_CPassword")
        self.urlclient = self._get_info_value(infos, "Zeendoc_URL_Client")
        self.classeur = self._get_info_value(infos, "Zeendoc_CLASSEUR")
        self.indexBAP = self._get_info_value(infos, "EBP_FOLDER_ID")
        self.indexPaiement = self._get_info_value(infos, "EBP_PAIEMENT")
        self.indexStatutPaiement = self._get_info_value(infos, "INDEX_STATUT_PAIEMENT")
        self.indexNumPiece = self._get_info_value(infos, "INDEX_NUM_PIECE")
        self.indexNumFacture = self._get_info_value(infos, "INDEX_NUM_FACTURE")
        self.right = None
        self.login()

    def _get_info_value(self, infos, key):
        """
        Fonction qui permet de récupérer la valeur d'une clé dans la liste des infos
        """
        for info in infos:
            if info["LibChamp"] == key:
                return info["Valeur"]
        return None

    def _create_soap_envelope(self, body):
        """
        Fonction qui permet de créer un enveloppe SOAP pour les requêtes
        """
        return f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    {body}
  </soap:Body>
</soap:Envelope>"""

    def login(self):
        """
        Fonction qui permet de se connecter à l'API Zeendoc
        """
        url = f"https://armoires.zeendoc.com/{self.urlclient}/ws/3_0/Zeendoc.php"
        body = f"""
        <login>
          <Login>{self.log}</Login>
          <Password></Password>
          <CPassword>{self.cpassword}</CPassword>
          <Access_token></Access_token>
        </login>"""
        payload = self._create_soap_envelope(body)
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "urn:Zeendoc#login",
            "Cookie": "ZeenDoc=c88d73cfd3fd7600bf9a6efb94e01599",
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.text

    def _post_request(self, body, action):
        """
        Helper function for sending SOAP requests
        """
        url = f"https://armoires.zeendoc.com/{self.urlclient}/ws/3_0/Zeendoc.php"
        payload = self._create_soap_envelope(body)
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"urn:Zeendoc#{action}",
            "Cookie": "ZeenDoc=c88d73cfd3fd7600bf9a6efb94e01599",
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.text

    def get_rights(self):
        """
        Fonction qui permet de récupérer les droits de l'utilisateur
        """
        body = """
        <getRights>
          <Get_ConfigSets></Get_ConfigSets>
          <Access_token></Access_token>
        </getRights>"""
        try:
            response_text = self._post_request(body, "getRights")
            root = ET.fromstring(response_text)
            json_response = root.find(".//jsonResponse").text
            self.right = json.loads(json_response)
            return self.right
        except (requests.RequestException, ET.ParseError, json.JSONDecodeError) as e:
            print(f"Erreur lors de la récupération des droits: {e}")
            return None

    def get_classeurs(self):
        """
        Fonction qui permet de récupérer les noms et id des classeurs de l'utilisateur
        """
        if not self.right:
            self.get_rights()
        return [
            {"Coll_Id": collection["Coll_Id"], "Label": collection["Label"]}
            for collection in self.right["Collections"]
        ]

    def get_index(self):
        """
        Fonction qui permet de récupérer les index de l'utilisateur
        """
        if not self.right:
            self.get_rights()

        return self.right["Collections"][0]["Index"] if self.right else None

    def get_id_index(self, index_libelle):
        """
        Fonction qui permet de récupérer l'id d'un index dans right
        en parcourant les collections puis les index
        """
        if not self.right:
            self.get_rights()
        for collection in self.right["Collections"]:
            for index in collection.get("Index", []):
                if index["Label"] == index_libelle:
                    return index["Index_Id"]
        return None

    def search_doc_by_custom(
        self, index_id, index_value, save_query_name="", wanted_columns=""
    ):
        """
        Fonction qui permet de chercher un document par un index custom
        """
        wanted_columns += index_id
        body = f"""
        <searchDoc>
          <Coll_Id>{self.classeur}</Coll_Id>
          <IndexList xsi:type="ArrayOfIndexDefinition">
            <Index>
                <Id>1</Id>
                <Label>{index_id}</Label>
                <Value>{index_value}</Value>
                <Operator>EQUALS</Operator>
            </Index>
          </IndexList>
          <Saved_Query_Name>{save_query_name}</Saved_Query_Name>
          <Wanted_Columns>{wanted_columns}</Wanted_Columns>
        </searchDoc>"""

        try:
            response_text = self._post_request(body, "searchDoc")
            root = ET.fromstring(response_text)
            json_response = root.find(".//jsonResponse").text
            return json.loads(json_response)
        except (requests.RequestException, ET.ParseError, json.JSONDecodeError) as e:
            print(f"Erreur lors de la recherche du document: {e}")
            return None

    def get_all_doc(self):
        """
        Fonction qui permet de récupérer tous les documents de l'utilisateur
        """
        body = f"""
        <searchDoc>
          <Coll_Id>{self.classeur}</Coll_Id>
          <IndexList/>
          <Saved_Query_Name></Saved_Query_Name>
          <Wanted_Columns>custom_n7</Wanted_Columns>
        </searchDoc>"""
        try:
            return self._post_request(body, "searchDoc")
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de tous les documents: {e}")
            return None

    def search_doc_by_id(self, doc_id):
        """
        Fonction qui permet de récupérer un document à partir de son id
        """
        body = f"""
        <searchDoc>
          <Coll_Id>{self.classeur}</Coll_Id>
          <IndexList>
            <Index>
                <Id>1</Id>
                <Label>Id</Label>
                <Value>{doc_id}</Value>
            </Index>
          </IndexList>
          <Saved_Query_Name></Saved_Query_Name>
          <Wanted_Columns>custom_n7</Wanted_Columns>
        </searchDoc>"""
        try:
            return self._post_request(body, "searchDoc")
        except requests.RequestException as e:
            print(f"Erreur lors de la recherche du document par ID: {e}")
            return None

    def get_doc_bap(self):
        """
        Fonction qui permet de récupérer les documents BAP
        """
        return self.search_doc_by_custom(self.indexBAP, "1")

    def get_doc_paiement(self):
        """
        Fonction qui permet de récupérer les documents de paiement
        """
        return self.search_doc_by_custom(self.indexPaiement, "0")

    def get_doc_ref(self, ref):
        """
        Fonction qui permet de récupérer un document par référence
        """
        try:
            res = self.search_doc_by_custom(self.indexStatutPaiement, ref)
            print(res)
            doc = res["Document"]
            res_id = doc[0]["Res_Id"]
            return res_id
        except (KeyError, IndexError, TypeError) as e:
            print(f"Erreur lors de la récupération du document par référence: {e}")
            return None

    def update_doc(self, coll_id, res_id, index_list, mode="UpdateGiven"):
        """
        Fonction qui permet de mettre à jour un document
        """
        index_xml = "".join(
            [
                f"""
            <Index>
                <Id>{index['Id']}</Id>
                <Label>{index['Label']}</Label>
                <Value>{index['Value']}</Value>
            </Index>"""
                for index in index_list
            ]
        )

        body = f"""
        <updateDoc>
          <Coll_Id>{coll_id}</Coll_Id>
          <Res_Id>{res_id}</Res_Id>
          <IndexList>
            {index_xml}
          </IndexList>
          <Mode>{mode}</Mode>
          <Access_token></Access_token>
        </updateDoc>"""

        # print("body: ", body)

        try:
            response_text = self._post_request(body, "updateDoc")
            root = ET.fromstring(response_text)
            json_response = root.find(".//jsonResponse").text

            # json_response:  {"Result":1}

            if json_response == '{"Result":1}':
                print(f"Document {res_id} mis à jour avec succès")

            return json.loads(json_response)
        except (requests.RequestException, ET.ParseError, json.JSONDecodeError) as e:
            print(f"Erreur lors de la mise à jour du document: {e}")
            return None

    def update_doc_paiement_by_ref(self, ref, index, value="1"):
        """
        Fonction qui permet de mettre à jour un document de paiement par référence
        ref: Référence du document
        index: L'index à mettre à jour
        value: La valeur de l'index à mettre à jour (par défaut "1")
        """
        try:
            # Vérifier que les paramètres critiques ne sont pas None
            if self.indexNumPiece is None or ref is None or self.classeur is None:
                raise ValueError("Un des paramètres critiques est None")

            # Recherche du document par référence
            res = self.search_doc_by_custom(self.indexNumPiece, ref)
            if not res or "Document" not in res:
                raise ValueError("Document non trouvé avec la référence fournie")

            doc = res["Document"]
            if not doc or "Res_Id" not in doc[0]:
                raise ValueError("Aucun Res_Id trouvé dans le document")

            res_id = doc[0]["Res_Id"]
            if res_id is None:
                raise ValueError("Le Res_Id est None")
            res_id = str(res_id)

            print("res_id: ", res_id)

            # Création de la liste des index à mettre à jour
            index_list = [{"Id": res_id, "Label": index, "Value": value}]

            # Mise à jour du document
            update_response = self.update_doc(
                coll_id=self.classeur, res_id=res_id, index_list=index_list
            )

            return update_response
        except (KeyError, IndexError, TypeError, ValueError) as e:
            print(f"Erreur lors de la mise à jour du document par référence: {e}")
            return None

    def update_doc_paiement_by_num_facture(self, num_facture, index, value="1", iteration=3):
        """
        Fonction qui permet de mettre à jour un document de paiement par numéro de facture
        num_facture: Numéro de la facture
        index: L'index à mettre à jour
        value: La valeur de l'index à mettre à jour (par défaut "1")
        """

        # print("update_doc_paiement_by_num_facture")
        # print("num_facture: ", num_facture)
        # print("index: ", index)
        # print("value: ", value)
        # print("self.indexNumFacture: ", self.indexNumFacture)
        # print("self.classeur: ", self.classeur)

        try:
            # Vérifier que les paramètres critiques ne sont pas None
            if (
                self.indexNumFacture is None
                or num_facture is None
                or self.classeur is None
            ):
                raise ValueError("Un des paramètres critiques est None")

            # Recherche du document par numéro de facture
            res = self.search_doc_by_custom(self.indexNumFacture, num_facture)


            # print("self.indexNumFacture: ", self.indexNumFacture)
            # print("num_facture: ", num_facture)
            # print("res: ", res)

            if not res or "Document" not in res:
                raise ValueError("Document non trouvé avec le numéro de facture fourni")

            doc = res["Document"]
            if not doc or "Res_Id" not in doc[0]:
                raise ValueError("Aucun Res_Id trouvé dans le document")

            res_id = doc[0]["Res_Id"]
            if res_id is None:
                raise ValueError("Le Res_Id est None")
            res_id = str(res_id)

            # Création de la liste des index à mettre à jour
            index_list = [{"Id": res_id, "Label": index, "Value": value}]

            # Mise à jour du document
            update_response = self.update_doc(
                coll_id=self.classeur, res_id=res_id, index_list=index_list
            )

            return update_response
        except (KeyError, IndexError, TypeError, ValueError) as e:
            # print(
            #     f"Erreur lors de la mise à jour du document par numéro de facture: {e}"
            # )

            if (iteration <= 0):
                return self.update_doc_paiement_by_num_facture(
                    num_facture, index, value, iteration - 1
                )
            return None

    def get_items_list(self, coll_id, column_name, only_deletable=50):
        """
        Méthode pour obtenir des éléments d'une liste déroulante
        """
        body = f"""
        <getItemsList>
          <Coll_Id>{coll_id}</Coll_Id>
          <Column_Name>{column_name}</Column_Name>
          <Only_Deletable>{only_deletable}</Only_Deletable>
          <ArrayOfListItemsIdOnly/>
          <Access_token></Access_token>
        </getItemsList>"""

        try:
            response_text = self._post_request(body, "getItemsList")
            root = ET.fromstring(response_text)
            json_response = root.find(".//jsonResponse").text

            return json.loads(json_response)["Items_List"]
        except (requests.RequestException, ET.ParseError, json.JSONDecodeError) as e:
            print(
                f"Erreur lors de la récupération des éléments de la liste déroulante: {e}"
            )
            return None

    def add_items_list(self, coll_id, column_name, items):
        """
        Méthode pour ajouter des éléments à une liste déroulante
        """
        items_xml = "".join(
            [
                f"""
            <List_Item>
                <Id></Id>
                <Label>{item}</Label>
            </List_Item>"""
                for item in items
            ]
        )

        body = f"""
        <AddItemsList xmlns="urn:Zeendoc">
            <Coll_Id>{coll_id}</Coll_Id>
            <Column_Name>{column_name}</Column_Name>
            <Items_List>
                {items_xml}
            </Items_List>
        </AddItemsList>"""

        try:
            print(
                "Request Body: ", body
            )  # Debug: afficher le corps de la requête pour débogage
            response_text = self._post_request(body, "AddItemsList")
            root = ET.fromstring(response_text)
            json_response = root.find(".//jsonResponse").text
            return json.loads(json_response)
        except (requests.RequestException, ET.ParseError, json.JSONDecodeError) as e:
            print(f"Erreur lors de l'ajout des éléments à la liste déroulante: {e}")
            return None
