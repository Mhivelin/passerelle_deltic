import unittest

from app import create_app
from app.models.client import Client


class TestModels(unittest.TestCase):
    """
    A test case class for testing the models in the client module.
    """

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_is_dict_get_Zeendoc(self):
        client = Client(1)
        client.clientZeendoc.BdGetClientZeendoc(1)
        res = client.BdGetClient(1)
        self.assertIsInstance(res, dict)

    def test_is_dict_get_EBP(self):
        client = Client(1)
        client.clientEBP.BdGetClientEBP(1)
        res = client.BdGetClient(1)
        self.assertIsInstance(res, dict)

    def test_setLastUpdatenow(self):
        client = Client(1)
        client.setLastUpdatenow()

    def test_routine(self):
        client = Client(1)
        client.routine()
