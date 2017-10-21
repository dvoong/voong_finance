# import datetime
# from unittest import mock
# from django.test import TestCase
# from voong_finance_app.tests import VoongTestCase
# from voong_finance_app.models import Transaction, Balance
# from voong_finance_app.utils import date_range
#
# class TestTransaction(TestCase):
#
#     def setUp(self):
#         self.type = 0
#         self.description = 'description'
#         self.date = datetime.date(2017, 1, 24)
#         self.size = 10
#
#     def test(self):
#
#         transaction = Transaction.objects.create(type=self.type, description=self.description, date=self.date, size=self.size)
#
# class TestBalanceLastEntry(TestCase):
#
#     def setUp(self):
#         pass
#
#     # returns the last entry
#     # when empty returns None
#
#     def test_returns_last_entry(self):
#         entry = Balance.objects.create(date=datetime.date(2017, 1, 24),
#                                        balance=10)
#
#         last_entry = Balance.last_entry()
#
#         self.assertEqual(entry, last_entry)
#
#
#     def test_returns_last_entry_when_there_are_multiple_entries(self):
#         entry1 = Balance.objects.create(date=datetime.date(2017, 1, 24),
#                                         balance=10)
#
#         entry2 = Balance.objects.create(date=datetime.date(2017, 1, 27),
#                                         balance
#                                         =10)
#
#         last_entry = Balance.last_entry()
#
#         self.assertEqual(entry2, last_entry)
#
#     def test_when_there_are_no_balance_entries_return_none(self):
#         last_entry = Balance.last_entry()
#
#         self.assertEqual(None, last_entry)
#
#
# class TestBalanceToDict(VoongTestCase):
#
#     def setUp(self):
#         self.patches = []
#         Balance.objects.create(date='2017-03-01', balance=10)
#         Balance.objects.create(date='2017-03-02', balance=11)
#         Balance.objects.create(date='2017-03-03', balance=12)
#         self.balances = Balance.objects.all()
#
#     def test(self):
#
#         output = Balance.to_dict(self.balances)
#         expected = {"columns": ["date", "balance"], "values": [["2017-03-01", 10.0], ["2017-03-02", 11.0], ["2017-03-03", 12.0]]}
#
#         self.assertEqual(output, expected)
#
# class TestBalanceGetBalances(VoongTestCase):
#
#     # filters balance entries between dates
#     # if all balance entries are found return balances
#     # if no balance entries are found, find the last entry
#     # if there is no last_entry calculate balances for the given dates with initial balance 0
#     # if there is a last_entry calculate balances from the last entry to the end of the specified date_range
#     # if there is a last_entry find the first_entry
#     # calculate the balances from the start to the first_entry
#     # append the before, middle and after balance entries
#     # return the balances
#
#     def setUp(self):
#         super(TestBalanceGetBalances, self).setUp()
#         self.start = datetime.date(2017, 3, 1)
#         self.end = datetime.date(2017, 3, 4)
#         self.dates = date_range(self.start, self.end)
#         self.balances = []
#         self.filter = self.mock('voong_finance_app.models.Balance.objects.filter')
#         self.filter.return_value.order_by.return_value = self.balances
#         self.last_entry = self.mock('voong_finance_app.models.Balance.last_entry')
#         self.calculate_balances = self.mock('voong_finance_app.models.Balance.calculate_balances')
#         self.first = self.mock('voong_finance_app.models.Balance.objects.first')
#
#     def test_filters_balance_entries_between_dates(self):
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         Balance.objects.filter.assert_called_once_with(date__gte=self.start, date__lt=self.end)
#
#     def test_if_all_balance_entries_are_found_return_balances(self):
#         self.balances = [1, 2, 3]
#         self.filter.return_value.order_by.return_value = self.balances
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.assertEqual(balances, self.balances)
#
#     def test_if_no_balance_entries_are_found_find_the_last_entry(self):
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.last_entry.assert_called_once_with()
#
#     def test_if_there_is_no_last_entry_calculate_balances_for_the_given_dates_with_initial_balance_0(self):
#         self.last_entry.return_value = None
#         calculated_balances = self.calculate_balances.return_value
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.calculate_balances.assert_called_once_with(starting_balance=0, dates=self.dates)
#         self.assertEqual(balances, calculated_balances)
#
#     def test_if_there_is_a_last_entry_calculate_balances_from_the_last_entry_to_the_end_of_the_specified_date_range(self):
#         last_entry = Balance(date=datetime.date(2017, 3, 1), balance=10)
#         dates = date_range(last_entry.date + datetime.timedelta(days=1), self.end)
#         self.last_entry.return_value = last_entry
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.assertEqual(self.calculate_balances.call_args_list[0][1], {'dates':dates, 'starting_balance':last_entry.balance})
#
#     def test_if_there_is_a_last_entry_find_the_first_entry(self):
#         last_entry = Balance(date=datetime.date(2017, 3, 1), balance=10)
#         self.last_entry.return_value = last_entry
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         Balance.objects.first.assert_called_once_with()
#
#     def test_calculate_the_balances_from_the_start_to_the_first_entry(self):
#         first_entry = Balance(date=datetime.date(2017, 1, 24), balance=10000)
#         last_entry = Balance(date=datetime.date(2017, 3, 1), balance=10)
#         self.first.return_value = first_entry
#         self.last_entry.return_value = last_entry
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.calculate_balances.assert_called_with(dates=date_range(self.start, first_entry.date), starting_balance=0)
#         self.assertEqual(self.calculate_balances.call_count, 2)
#
#     def test_returns_beginning_middle_and_end_balances(self):
#         first_entry = Balance(date=datetime.date(2017, 1, 24), balance=10000)
#         last_entry = Balance(date=datetime.date(2017, 3, 1), balance=10)
#         self.first.return_value = first_entry
#         self.last_entry.return_value = last_entry
#         Balance.objects.filter.return_value.order_by.return_value = ['a']
#         Balance.calculate_balances.side_effect = [['b'], ['c']]
#
#         balances = Balance.get_balances(self.start, self.end)
#
#         self.assertEqual(balances, ['c', 'a', 'b'])
#
