import json
from django.test import TestCase
from django.urls import resolve
from .views import initialise_balance

# Create your tests here.
class TestInitialiseBalance(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_resolution(self):

        resolver = resolve('/api/initialise-balance')
        self.assertEqual(resolver.func, initialise_balance)

    def test_returns_the_balance_in_json_object(self):

        response = self.client.post('/api/initialise-balance', {'balance': 4344.40})
        expected = {'date': 'TODO', 'balance': 4344.40}
        self.assertEqual(expected, response.json(), 'TODO')
