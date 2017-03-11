import datetime
import json
from datetime import date
from unittest import mock
from django.test import TestCase
from django.urls import resolve
from .views import initialise_balance, transaction_form
from voong_finance_app import  views

# Create your tests here.
@mock.patch('voong_finance_app.views.datetime.date')
class TestInitialiseBalance(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_resolution(self, mock_date):

        resolver = resolve('/api/initialise-balance')
        self.assertEqual(resolver.func, initialise_balance)

    def test_returns_the_balance_in_json_object(self, mock_date):
        expected_date = date(2017, 1, 24)
        mock_date.today.return_value = expected_date
        response = self.client.post('/api/initialise-balance', {'balance': 4344.40})
        expected = {'date': expected_date.isoformat(), 'balance': 4344.40}
        self.assertEqual(expected, response.json())

    def test_if_date_argument_exists_returns_the_same_date(self, mock_date):
        data = {'balance': 4344.40, 'date': '2017-01-24'}
        response = self.client.post('/api/initialise-balance', data)
        self.assertEqual(response.json(), data)
        mock_date.assert_not_called()

@mock.patch('voong_finance_app.views.TransactionForm')
@mock.patch('voong_finance_app.views.render')
class TestTransactionForm(TestCase):

    def setUp(self):
        self.url = '/api/transaction-form'
        self.template_name = 'voong_finance_app/transaction-form.html'

    def test_url_resolution(self, render, TransactionForm):
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, transaction_form)

    def test_return_rendered_transaction_template(self, render, TransactionForm):

        request = mock.Mock()
        expected = mock.Mock()
        render.return_value = expected

        response = views.transaction_form(request)
        
        self.assertEqual(response, expected)

    def test_call_render_with_transaction_form_object_in_the_context(self, render, TransactionForm):

        request = mock.Mock()
        template_name = self.template_name
        context = {'form': str(TransactionForm.return_value)}
        
        response = views.transaction_form(request)
        
        render.assert_called_with(request, template_name, context)
