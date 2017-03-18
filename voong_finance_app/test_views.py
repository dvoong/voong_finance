import datetime
import json
from datetime import date
from unittest import mock
from django.test import TestCase, Client
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
        self.TransactionPatch = mock.patch('voong_finance_app.views.Transaction')
        self.Transaction = self.TransactionPatch.start()
        self.RepeatTransactionPatch = mock.patch('voong_finance_app.views.RepeatTransaction')
        self.RepeatTransaction = self.RepeatTransactionPatch.start()
        self.BalancePatch = mock.patch('voong_finance_app.views.Balance')
        self.Balance = self.BalancePatch.start()
        self.date = datetime.date(2017, 1, 24)
        self.end_date = datetime.date(2017, 12, 24)
        self.post_data = {
            'type': 0,
            'description': 'description',
            'size': 15,
            'date_year': self.date.year,
            'date_month': self.date.month,
            'date_day': self.date.day,
            'chart_date_start': '2017-01-21',
            'chart_date_end': '2017-02-17',
        }
        self.repeat_post_data = {
            'type': 0,
            'description': 'description',
            'frequency': 0,
            'size': 15,
            'repeats': 'on',
            'date_year': self.date.year,
            'date_month': self.date.month,
            'date_day': self.date.day,
            'end_date_year': self.end_date.year,
            'end_date_month': self.end_date.month,
            'end_date_day': self.end_date.day,
            'chart_date_start': '2017-01-21',
            'chart_date_end': '2017-02-17',
        }
        self.post_request = mock.Mock(method='POST', POST=self.post_data)
        self.JsonResponse_patch = mock.patch('voong_finance_app.views.JsonResponse')
        self.JsonResponse = self.JsonResponse_patch.start()

    def tearDown(self):
        self.TransactionPatch.stop()
        self.RepeatTransactionPatch.stop()
        self.BalancePatch.stop()
        self.JsonResponse_patch.stop()

    def test_url_resolution(self, render, TransactionForm):
        resolver = resolve(self.url)
        self.assertEqual(resolver.func, transaction_form)

    def test_return_rendered_transaction_template(self, render, TransactionForm):

        request = mock.Mock(method='GET')
        expected = mock.Mock()
        render.return_value = expected

        response = views.transaction_form(request)
        
        self.assertEqual(response, expected)

    def test_call_render_with_transaction_form_object_in_the_context(self, render, TransactionForm):

        request = mock.Mock(method='GET')
        template_name = self.template_name
        context = {'form': str(TransactionForm.return_value)}
        
        response = views.transaction_form(request)

        TransactionForm.assert_called_once_with(initial={'date': datetime.date.today()})
        render.assert_called_with(request, template_name, context)

    def test_called_with_post_then_creates_a_new_transaction_object(self, render, TransactionForm):
        
        views.transaction_form(self.post_request)
        
        self.assertEqual(self.Transaction.objects.create.called, True)

    def test_if_repeat_not_in_data_then_creates_one_transaction(self, render, TransactionForm):

        views.transaction_form(self.post_request)

        self.Transaction.objects.create.assert_called_with(type=self.post_data['type'],
                                                           description=self.post_data['description'],
                                                           date=self.date,
                                                           size=-1 * self.post_data['size'])
        
    def test_if_repeat_is_on_then_creates_a_repeat_transaction_object(self, render, TransactionForm):
        post_data = self.repeat_post_data
        self.post_request.POST = post_data

        views.transaction_form(self.post_request)

        self.RepeatTransaction.assert_called_with(date=self.date,
                                                  type=post_data['type'],
                                                  description=post_data['description'],
                                                  size=post_data['size'],
                                                  frequency=post_data['frequency'],
                                                  end_date=self.end_date)

    def test_if_repeat_is_on_then_creates_transactions_up_to_the_latest_balance_entry(self, render, TransactionForm):
        repeat_transaction = mock.Mock()
        last_entry = mock.Mock()
        self.post_request.POST = self.repeat_post_data
        self.RepeatTransaction.return_value = repeat_transaction
        self.Balance.last_entry.return_value = last_entry

        views.transaction_form(self.post_request)

        repeat_transaction.create_transactions.assert_called_with(repeat_transaction.date, last_entry.date)

    ####
    def test_recalculates_balances_from_transaction_date_to_the_end_of_the_chart_range(self, render, TransactionForm):

        views.transaction_form(self.post_request)

        self.Balance.recalculate.assert_called_once_with(datetime.date(2017, 1, 24), datetime.date(2017, 2, 18))

    def test_if_repeats_is_false_then_dont_create_repeat_transaction(self, render, TransactionForm):
        views.transaction_form(self.post_request)

        self.RepeatTransaction.assert_not_called()

class TestTransactionFormIntegration(TestCase):

    def setUp(self):

        self.client = Client()

    def test(self):

        data = {
            'date_year': 2017,
            'date_month': 1,
            'date_day': 24,
            'description': 'description',
            'type': 0,
            'size': 10,
            'chart_date_start': '2017-01-21',
            'chart_date_end': '2017-02-17'
        }

        response = self.client.post('/api/transaction-form', data)
        response = response.json()

        self.assertEqual(response['columns'], ['date', 'balance'])
        self.assertEqual(response['values'][0][0], '2017-01-24')
        self.assertEqual(response['values'][0][1], -10)
        self.assertEqual(response['values'][-1][0], '2017-02-17')
        self.assertEqual(response['values'][-1][1], -10)

print('test_views')        
