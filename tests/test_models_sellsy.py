import unittest

from app import create_app
from app.models.sellsy import Sellsy


class TestModels(unittest.TestCase):
    """
    Classe de cas de test pour vérifier le bon fonctionnement des modèles relatifs à EBP.
    """

    def setUp(self):
        """
        Initialise l'application et le contexte avant chaque test.
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Nettoie le contexte après chaque test.
        """
        self.app_context.pop()

    def test_init(self):
        """
        Teste l'initialisation de l'objet Sellsy.
        """

        # Test
        sellsy = Sellsy(1)
        self.assertEqual(sellsy.databaseId, 1)

    # def test_get_invoice(self):
    #     """
    #     Teste la récupération des factures.
    #     """
    #     sellsy = Sellsy(1)
    #     print(sellsy.get_invoices())

    # def test_get_paid_invoices(self):
    #     """
    #     Teste la récupération des factures payées.
    #     """
    #     sellsy = Sellsy(1)
    #     print(sellsy.get_paid_invoices())


    def test_update_invoice_smart_tags(self):
        """
        Teste la mise à jour des tags d'une facture.
        """
        sellsy = Sellsy(1)
        tags = [{"value": "paiement exporté"}]  # Tags formatés correctement
        print(
            "update_invoice_smart_tags",
            sellsy.update_invoice_smart_tags(51134735, tags),
        )





    # def test_get_invoice_payments(self):
    #     """
    #     Teste la récupération des paiements d'une facture.
    #     """
    #     sellsy = Sellsy(1)
    #     print("Payments:", sellsy.get_invoice_payments(51134735))

    # def test_get_paid_invoices_with_last_payment(self):
    #     """
    #     Teste la récupération des factures payées avec leur dernier paiement.
    #     """
    #     sellsy = Sellsy(1)
    #     print(
    #         "test_get_paid_invoices_with_last_payment",
    #         sellsy.get_paid_invoices_with_last_payment(),
    #     )

    #     # Example usage
    #     # sellsy_api = Sellsy(client_id, client_secret)
