from app import create_app
from flask_testing import TestCase


class TestRoutes(TestCase):

    def create_app(self):
        # Configurez votre application Flask pour les tests
        app = create_app()
        app.config["TESTING"] = True
        return app

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Liste des Clients", response.data.decode())











if __name__ == "__main__":
    import unittest

    unittest.main()
