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
        self.request = mock.Mock()
        self.request.POST = {'date': '2017-01-24', 'balance': 4344.40}
        self.BalancePatch = mock.patch('voong_finance_app.views.Balance')
        self.Balance = self.BalancePatch.start()
        self.Balance.objects.create = mock.Mock()
        self.JsonResponsePatch = mock.patch('voong_finance_app.views.JsonResponse')
        self.JsonResponse = self.JsonResponsePatch.start()
        self.JsonResponse.return_value = mock.Mock()

    def tearDown(self):
        self.BalancePatch.stop()
        self.JsonResponsePatch.stop()

    def test_url_resolution(self, mock_date):

        resolver = resolve('/api/initialise-balance')
        self.assertEqual(resolver.func, initialise_balance)

    def test_if_date_argument_not_passed_use_today(self, mock_date):
        expected_date = datetime.datetime(2017, 1, 24).date()
        mock_date.today.return_value = expected_date
        request = mock.Mock()
        request.POST = {'balance': 4344.40}
        
        initialise_balance(request)
        self.assertEqual(self.Balance.objects.create.call_args_list[0][1], {'date': expected_date, 'balance': 4344.40})

    def test_if_date_argument_exists_returns_the_same_date(self, mock_date):
        initialise_balance(self.request)
                         
        self.assertEqual(self.Balance.objects.create.call_args_list[0][1], {'date': datetime.datetime(2017, 1, 24).date(), 'balance': 4344.40})
        self.assertEqual(self.Balance.objects.create.call_args_list[-1][1], {'date': datetime.datetime(2017, 2, 20).date(), 'balance': 4344.40})

    def test_creates_balance_objects_from_date_to_four_weeks_ahead(self, mock_date):
        initialise_balance(self.request)

        self.assertEqual(self.Balance.objects.create.call_count, 28)

    def test_returns_json_response(self, mock_date):
        response = initialise_balance(self.request)

        self.assertEqual(response, self.JsonResponse.return_value)

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

    def test_called_with_post_then_creates_a_new_transaction_object(self, render, TransactionForm):
        # creates a transaction object
        # calculates the balance from the transaction_date till the latest date
        self.assertTrue(False, 'todo')
