import datetime
import json
from datetime import date
from unittest import mock
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

    @mock.patch('voong_finance_app.views.datetime.date')
    def test_returns_the_balance_in_json_object(self, mock_date):
        expected_date = date(2017, 1, 24)
        mock_date.today.return_value = expected_date
        response = self.client.post('/api/initialise-balance', {'balance': 4344.40})
        expected = {'date': expected_date.isoformat(), 'balance': 4344.40}
        self.assertEqual(expected, response.json(), 'TODO')
