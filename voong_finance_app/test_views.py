from django.test import TestCase, Client
from django.urls import resolve
from voong_finance_app import views
from voong_finance_app.models import User

class TestRegistration(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        self.assertEqual(resolve('/registration').func, views.registration)

    def test_template(self):
        response = self.client.get('/registration')
        self.assertTemplateUsed(response, 'voong_finance_app/registration.html')

class TestSignin(TestCase):

    def setUp(self):
        self.client = Client()

    def test_url_resolve(self):
        self.assertEqual(resolve('/signin').func, views.signin)

    def test_template(self):
        response = self.client.get('/signin')
        self.assertTemplateUsed(response, 'voong_finance_app/signin.html')

    def test_check_credentials(self):
        user = User.objects.create(email='voong.david@gmail.com', password='password')
        response = self.client.post('/signin', data={'email': 'voong.david@gmail.com', 'password': 'password'})
        self.assertRedirects(response, '/')

# import datetime
# import json
# from datetime import date
# from unittest import mock
# from django.test import TestCase, Client
# from django.urls import resolve
# from .views import initialise_balance, transaction_form, home, get_balances
# from voong_finance_app.tests import VoongTestCase
# from voong_finance_app import  views
#
# # Create your tests here.
# class TestHome(VoongTestCase):
#
#     def setUp(self):
#         super(TestHome, self).setUp()
#         self.request = mock.Mock()
#         self.render = self.mock('voong_finance_app.views.render')
#         self.Balance = self.mock('voong_finance_app.views.Balance')
#         self.dates = mock.Mock()
#         self.get_month_dates = self.mock('voong_finance_app.views.get_month_dates')
#         self.get_month_dates.return_value = self.dates
#
#     def test_url_resolution(self):
#
#         resolver = resolve('/api/')
#
#         self.assertEqual(resolver.func, home)
#
#     def test_if_no_balance_entries_exist_return_welcome_page(self):
#         self.Balance.objects.all.return_value = []
#
#         home(self.request)
#
#         self.render.assert_called_once_with(self.request, 'voong_finance_app/welcome.html', {'dates': self.dates})
#
#
#     def test_if_balance_entries_do_exist_return_home_page(self):
#         self.Balance.objects.all.return_value = [mock.Mock()]
#
#         home(self.request)
#
#         self.render.assert_called_once_with(self.request, 'voong_finance_app/home.html', {'dates': self.dates})
#
#     def test_get_dates_for_this_month(self):
#
#         home(self.request)
#
#         self.get_month_dates.assert_called_once_with(datetime.date.today())
#
# class TestInitialiseBalance(VoongTestCase):
#
#     def setUp(self):
#         super(TestInitialiseBalance, self).setUp()
#         self.request = mock.Mock()
#         self.request.POST = {'date': '2017-01-24', 'balance': 4344.40}
#         self.Balance = self.mock('voong_finance_app.views.Balance')
#         self.Balance.objects.create = mock.Mock()
#         self.date_module = self.mock('voong_finance_app.views.datetime.date')
#         self.convert_date_string = self.mock('voong_finance_app.views.convert_date_string')
#         self.JsonResponse = self.mock('voong_finance_app.views.JsonResponse')
#         self.Transaction = self.mock('voong_finance_app.views.Transaction')
#
#     def test_url_resolution(self):
#
#         resolver = resolve('/api/initialise-balance')
#         self.assertEqual(resolver.func, initialise_balance)
#
#     def test_if_date_argument_not_passed_use_today(self):
#         self.request.POST = {'balance': 4344.40}
#
#         initialise_balance(self.request)
#
#         self.assertEqual(self.date_module.today.call_args_list[0][0], ())
#
#     def test_if_date_argument_exists_convert_to_date_object(self):
#         initialise_balance(self.request)
#
#         self.convert_date_string.assert_called_once_with(self.request.POST['date'])
#
#     def test_creates_balance_initialisation_transaction(self):
#         initialise_balance(self.request)
#
#         self.Transaction.objects.create.assert_called_once_with(type='Initialisation',
#                                                                 description='Initialisation',
#                                                                 date=self.convert_date_string.return_value,
#                                                                 size=self.request.POST['balance'])
#
#     def test_gets_balances_for_28_days_ahead(self):
#         start = datetime.date(2017, 4, 1)
#         end = start + datetime.timedelta(days=28)
#         self.convert_date_string.return_value = start
#
#         initialise_balance(self.request)
#
#         self.Balance.get_balances.assert_called_once_with(start=start, end=end)
#
#     def test_returns_json_response(self):
#         response = initialise_balance(self.request)
#
#         self.assertEqual(response, self.JsonResponse.return_value)
#         self.Balance.to_dict.assert_called_once_with(self.Balance.get_balances.return_value)
#         self.JsonResponse.assert_called_once_with(self.Balance.to_dict.return_value)
#
# @mock.patch('voong_finance_app.views.TransactionForm')
# @mock.patch('voong_finance_app.views.render')
# class TestTransactionForm(TestCase):
#
#     def setUp(self):
#         self.url = '/api/transaction-form'
#         self.template_name = 'voong_finance_app/transaction-form.html'
#         self.TransactionPatch = mock.patch('voong_finance_app.views.Transaction')
#         self.Transaction = self.TransactionPatch.start()
#         self.RepeatTransactionPatch = mock.patch('voong_finance_app.views.RepeatTransaction')
#         self.RepeatTransaction = self.RepeatTransactionPatch.start()
#         self.BalancePatch = mock.patch('voong_finance_app.views.Balance')
#         self.Balance = self.BalancePatch.start()
#         self.date = datetime.date(2017, 1, 24)
#         self.end_date = datetime.date(2017, 12, 24)
#
#         self.post_data = {
#             'type': 1,
#             'description': 'description',
#             'size': 15,
#             'date_year': self.date.year,
#             'date_month': self.date.month,
#             'date_day': self.date.day,
#             'chart_date_start': '2017-01-21',
#             'chart_date_end': '2017-02-17',
#         }
#
#         self.repeat_post_data = {
#             'type': 1,
#             'description': 'description',
#             'frequency': 0,
#             'size': 15,
#             'repeats': 'on',
#             'date_year': self.date.year,
#             'date_month': self.date.month,
#             'date_day': self.date.day,
#             'end_date_year': self.end_date.year,
#             'end_date_month': self.end_date.month,
#             'end_date_day': self.end_date.day,
#             'chart_date_start': '2017-01-21',
#             'chart_date_end': '2017-02-17',
#         }
#         self.post_request = mock.Mock(method='POST', POST=self.post_data)
#         self.JsonResponse_patch = mock.patch('voong_finance_app.views.JsonResponse')
#         self.JsonResponse = self.JsonResponse_patch.start()
#
#     def tearDown(self):
#         self.TransactionPatch.stop()
#         self.RepeatTransactionPatch.stop()
#         self.BalancePatch.stop()
#         self.JsonResponse_patch.stop()
#
#     def test_url_resolution(self, render, TransactionForm):
#         resolver = resolve(self.url)
#         self.assertEqual(resolver.func, transaction_form)
#
#     def test_return_rendered_transaction_template(self, render, TransactionForm):
#
#         request = mock.Mock(method='GET')
#         expected = mock.Mock()
#         render.return_value = expected
#
#         response = views.transaction_form(request)
#
#         self.assertEqual(response, expected)
#
#     def test_call_render_with_transaction_form_object_in_the_context(self, render, TransactionForm):
#
#         request = mock.Mock(method='GET')
#         template_name = self.template_name
#         context = {'form': str(TransactionForm.return_value)}
#
#         response = views.transaction_form(request)
#
#         TransactionForm.assert_called_once_with(initial={'date': datetime.date.today()})
#         render.assert_called_with(request, template_name, context)
#
#     def test_called_with_post_then_creates_a_new_transaction_object(self, render, TransactionForm):
#
#         views.transaction_form(self.post_request)
#
#         self.assertEqual(self.Transaction.objects.create.called, True)
#
#     def test_if_repeat_not_in_data_then_creates_one_transaction(self, render, TransactionForm):
#
#         views.transaction_form(self.post_request)
#
#         self.Transaction.objects.create.assert_called_with(type=self.post_data['type'],
#                                                            description=self.post_data['description'],
#                                                            date=self.date,
#                                                            size=-1 * self.post_data['size'])
#
#     def test_recalculates_balances_from_transaction_date_to_the_end_of_the_chart_range(self, render, TransactionForm):
#
#         views.transaction_form(self.post_request)
#
#         self.Balance.recalculate.assert_called_once_with(datetime.date(2017, 1, 24), datetime.date(2017, 2, 18))
#
#     def test_if_repeats_is_false_then_dont_create_repeat_transaction(self, render, TransactionForm):
#         views.transaction_form(self.post_request)
#
#         self.RepeatTransaction.assert_not_called()
#
# class TestTransactionFormIntegration(TestCase):
#
#     def setUp(self):
#
#         self.client = Client()
#
#     def test(self):
#
#         data = {
#             'date_year': 2017,
#             'date_month': 1,
#             'date_day': 24,
#             'description': 'description',
#             'type': 1,
#             'size': 10,
#             'chart_date_start': '2017-01-21',
#             'chart_date_end': '2017-02-17'
#         }
#
#         response = self.client.post('/api/transaction-form', data)
#         response = response.json()
#
#         self.assertEqual(response['columns'], ['date', 'balance'])
#         self.assertEqual(response['values'][0][0], '2017-01-24')
#         self.assertEqual(response['values'][0][1], -10)
#         self.assertEqual(response['values'][-1][0], '2017-02-17')
#         self.assertEqual(response['values'][-1][1], -10)
#
# class TestGetBalances(VoongTestCase):
#
#     def setUp(self):
#         super(TestGetBalances, self).setUp()
#         self.Balance = self.mock('voong_finance_app.views.Balance')
#         self.balances = [{'date': '2017-03-01', 'balance': 1},
#                          {'date': '2017-03-03', 'balance': 2},
#                          {'date': '2017-03-03', 'balance': 3}]
#         self.Balance.get_balances.return_value = self.balances
#         self.dict_ = mock.Mock()
#         self.Balance.to_dict.return_value = self.dict_
#         self.json_response = mock.Mock()
#         self.JsonResponse = self.mock('voong_finance_app.views.JsonResponse')
#         self.JsonResponse.return_value = self.json_response
#         self.request = mock.Mock()
#
#     def test_url_resolution(self):
#
#         resolver = resolve('/api/get-balances')
#
#         self.assertEqual(resolver.func, get_balances)
#
#     def test(self):
#         balances = get_balances(self.request)
#
#         today = datetime.date.today()
#         start = today - datetime.timedelta(days=13)
#         end = today + datetime.timedelta(days=15)
#         self.Balance.get_balances.assert_called_once_with(start=start, end=end)
#         self.Balance.to_dict.assert_called_once_with(self.balances)
#         self.JsonResponse.assert_called_once_with(self.dict_)
#         self.assertEqual(balances, self.json_response)

    

