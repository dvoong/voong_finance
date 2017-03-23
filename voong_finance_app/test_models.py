import datetime
from unittest import mock
from django.test import TestCase
from voong_finance_app.tests import VoongTestCase
from voong_finance_app.models import Transaction, Balance
from voong_finance_app.utils import date_range

class TestTransaction(TestCase):

    def setUp(self):
        self.type = 0
        self.description = 'description'
        self.date = datetime.date(2017, 1, 24)
        self.size = 10

    def test(self):

        transaction = Transaction.objects.create(type=self.type, description=self.description, date=self.date, size=self.size)

class TestBalanceRecalculate(TestCase):

    # deletes all balance entries on and after the start date
    # generates a date_range
    # calculates an initial balance
    # calls the calculate_balance function with an output object, initial_balance and dates
    # returns the balance_objects

    def setUp(self):

        self.filter_patch = mock.patch('voong_finance_app.models.Balance.objects.filter')
        self.filter = self.filter_patch.start()
        self.filter.return_value = mock.Mock()
        self.calculate_balances_patch = mock.patch('voong_finance_app.models.Balance.calculate_balances')
        self.calculate_balances = self.calculate_balances_patch.start()
        self.calculate_balances.return_value = mock.Mock()
        self.last_entry_patch = mock.patch('voong_finance_app.models.Balance.last_entry')
        self.last_entry = self.last_entry_patch.start()
        self.date_range_patch = mock.patch('voong_finance_app.models.date_range')
        self.date_range = self.date_range_patch.start()
        self.start = datetime.date(2017, 3, 1)
        self.end = datetime.date(2017, 3, 8)

    def tearDown(self):
        self.filter_patch.stop()
        self.calculate_balances_patch.stop()
        self.last_entry_patch.stop()
        self.date_range_patch.stop()
        
    def test_filters_all_balance_entries_on_and_after_the_start_date(self):
        
        balances = Balance.recalculate(self.start, self.end)

        self.filter.assert_called_once_with(date__gte=self.start)
        
    def test_deletes_filtered_balance_entries(self):
        
        balances = Balance.recalculate(self.start, self.end)

        self.filter.return_value.delete.assert_called_once_with()
    
    def test_generates_a_date_range_given_by_start_and_end_dates(self):

        balances = Balance.recalculate(self.start, self.end)

        self.date_range.assert_called_once_with(self.start, self.end)

    def test_get_the_last_balance_before_the_start_date(self):

        balances = Balance.recalculate(self.start, self.end)

        self.last_entry.assert_called_once_with()

    def test_returns_balance_objects(self):

        balances = Balance.recalculate(self.start, self.end)

        self.assertEqual(balances, self.calculate_balances.return_value)

    def test_if_last_entry_exists_call_calulate_balances_with_its_balance(self):

        balances = Balance.recalculate(self.start, self.end)

        self.calculate_balances.assert_called_once_with({'columns': ['date', 'balance'], 'values': []}, self.last_entry.return_value.balance, self.date_range.return_value)

    def test_if_last_entry_does_not_exist_call_calulate_balances_with_its_balance(self):
        self.last_entry.return_value = None

        balances = Balance.recalculate(self.start, self.end)

        self.calculate_balances.assert_called_once_with({'columns': ['date', 'balance'], 'values': []}, 0, self.date_range.return_value)

        
class TestBalanceLastEntry(TestCase):

    def setUp(self):
        pass

    # returns the last entry
    # when empty returns None
    
    def test_returns_last_entry(self):
        entry = Balance.objects.create(date=datetime.date(2017, 1, 24),
                                       balance=10)
        
        last_entry = Balance.last_entry()

        self.assertEqual(entry, last_entry)

    
    def test_returns_last_entry_when_there_are_multiple_entries(self):
        entry1 = Balance.objects.create(date=datetime.date(2017, 1, 24),
                                        balance=10)

        entry2 = Balance.objects.create(date=datetime.date(2017, 1, 27),
                                        balance
                                        =10)
        
        last_entry = Balance.last_entry()
    
        self.assertEqual(entry2, last_entry)

    def test_when_there_are_no_balance_entries_return_none(self):
        last_entry = Balance.last_entry()

        self.assertEqual(None, last_entry)
        

class TestBalanceCalculateBalances(VoongTestCase):

    # if the number of dates is 0 then return the output
    # calculate_the_balance_for_the_first_date
    # add the balance to the output
    # calls calculate_balance for the remaning dates

    def setUp(self):
        self.patches = []
        self.Transaction_patch = mock.patch('voong_finance_app.models.Transaction')
        self.Transaction = self.Transaction_patch.start()
        self.Sum_patch = mock.patch('voong_finance_app.models.Sum')
        self.Sum = self.Sum_patch.start()
        self.input = {'columns': ['date', 'balance'], 'values': [['2017-02-28', 7]]}
        self.initial_balance = 7
        self.dates = [datetime.date(2017, 3, 1)]
        self.objects = self.mock('voong_finance_app.models.Balance.objects')

    def tearDown(self):
        super(TestBalanceCalculateBalances, self).tearDown()
        self.Transaction_patch.stop()
        self.Sum_patch.stop()

    def test_if_the_number_of_dates_is_0_then_return_the_output(self):

        input = {'columns': ['date', 'balance'], 'values': [['2017-03-01', 10]]}
        initial_balance = 7
        dates = []
        
        output = Balance.calculate_balances(input, initial_balance, dates)

        self.assertEqual(output, input)

    def test_calculate_the_balance_for_the_first_date(self):

        input = {'columns': ['date', 'balance'], 'values': [['2017-02-28', 7]]}
        initial_balance = 7
        dates = [datetime.date(2017, 3, 1), datetime.date(2017, 3, 2)]
        transactions = mock.Mock(__len__=mock.Mock(return_value=1))
        self.Transaction.objects.filter.return_value = transactions
        transactions.aggregate.return_value = {'size__sum': -4}
        
        output = Balance.calculate_balances(input, initial_balance, dates)

        self.Transaction.objects.filter.assert_called_with(date=dates[1])
        self.assertEqual(self.Transaction.objects.filter.call_count, 2)
        transactions.aggregate.assert_called_with(self.Sum.return_value)
        self.Sum.assert_called_with('size')

    def test_add_the_balance_to_the_output(self):

        transactions = mock.Mock(__len__=mock.Mock(return_value=1))
        self.Transaction.objects.filter.return_value = transactions
        transactions.aggregate.return_value = {'size__sum': -4}
        
        output = Balance.calculate_balances(self.input, self.initial_balance, self.dates)

        self.assertEqual(output['values'][1][0], '2017-03-01')
        self.assertEqual(output['values'][1][1], 3)

    def test_creates_balance_objects(self):

        output = Balance.calculate_balances(self.input, self.initial_balance, self.dates)

        self.objects.create.assert_called_once_with(date=self.dates[0], balance=self.initial_balance)

class TestBalanceToDict(VoongTestCase):

    def setUp(self):
        self.patches = []
        Balance.objects.create(date='2017-03-01', balance=10)
        Balance.objects.create(date='2017-03-02', balance=11)
        Balance.objects.create(date='2017-03-03', balance=12)
        self.balances = Balance.objects.all()

    def test(self):

        output = Balance.to_dict(self.balances)
        expected = {"columns": ["date", "balance"], "values": [["2017-03-01", 10.0], ["2017-03-02", 11.0], ["2017-03-03", 12.0]]}

        self.assertEqual(output, expected)
        
class TestBalanceGetBalances(VoongTestCase):

    # filters balance entries between dates
    # if no balance entries are found, find the last entry
    # if there is no last_entry calculate balances for the given dates with initial balance 0
    # if there is a last_entry calculate balances from the last entry to the end of the specified date_range
    # if a balance_entry_was_found_find any missing dates
    # if no missing dates return the balance entries
    # if some dates are missing, then
    # find the first filtered balance and calculate the balances from the last_entry to it, then
    # find the last filtered balance and calculate the balances from the last filtered balance to specified end date
    # return a list of balances

    def setUp(self):
        super(TestBalanceGetBalances, self).setUp()
        self.start = datetime.date(2017, 3, 1)
        self.end = datetime.date(2017, 3, 4)
        self.dates = date_range(self.start, self.end)
        self.balances = []
        self.filter = self.mock('voong_finance_app.models.Balance.objects.filter')
        self.filter.return_value = self.balances
        self.find_missing_dates = self.mock('voong_finance_app.models.Balance.find_missing_dates')
        self.last_entry = self.mock('voong_finance_app.models.Balance.last_entry')
        self.calculate_balances = self.mock('voong_finance_app.models.Balance.calculate_balances')

    def test_filters_balance_entries_between_dates(self):

        balances = Balance.get_balances(self.start, self.end)

        Balance.objects.filter.assert_called_once_with(date__gte=self.start, date__lt=self.end)

    def test_if_no_balance_entries_are_found_find_the_last_entry(self):

        balances = Balance.get_balances(self.start, self.end)

        self.last_entry.assert_called_once_with()

    def test_if_there_is_no_last_entry_calculate_balances_for_the_given_dates_with_initial_balance_0(self):
        self.last_entry.return_value = None

        balances = Balance.get_balances(self.start, self.end)

        self.calculate_balances.assert_called_once_with(initial_balance=0, dates=self.dates)
        
    def test_find_the_missing_dates(self):

        balances = Balance.get_balances(self.start, self.end)

        Balance.find_missing_dates.assert_called_once_with(self.dates, self.balances)

    def test_if_no_missing_dates_return_the_balance_entries(self):
        self.balances = [1, 2, 3]
        self.filter.return_value = self.balances
        
        balances = Balance.get_balances(self.start, self.end)

        self.assertEqual(balances, self.balances)
    

    # def setUp(self):
    #     self.patches = []
    #     self.objects = self.mock('voong_finance_app.models.Balance.objects')
    #     self.objects.filter.return_value = mock.Mock()
    #     self.start = datetime.date(2017, 3, 1)
    #     self.end = datetime.date(2017, 3, 4)
    #     self.len = self.mock('voong_finance_app.models.len')
    #     self.set = self.mock('voong_finance_app.models.set')
    #     self.map = self.mock('voong_finance_app.models.map')
    #     self.last_entry_ = Balance(date=datetime.date(2017, 2, 26), balance=10)
    #     self.last_entry = self.mock('voong_finance_app.models.Balance.last_entry')
    #     self.last_entry.return_value = self.last_entry_
    #     self.calculate_balances = self.mock('voong_finance_app.models.Balance.calculate_balances')
    #     self.date_range = self.mock('voong_finance_app.models.date_range')

    # def test_all_entries_exist(self):
    #     self.len.return_value = 3

    #     balances = Balance.get_balances(start=self.start, end=self.end)

    #     self.objects.filter.assert_called_once_with(date__gte=self.start, date__lt=self.end)
    #     self.objects.filter().order_by.assert_called_once_with('date')
    #     self.assertEqual(balances, self.objects.filter().order_by.return_value)

    # def test_not_all_entries_exist(self):
    #     self.len.return_value = 2
    #     output = {'columns': ['date', 'balance'], 'values': []}

    #     balances = Balance.get_balances(self.start, self.end)

    #     self.last_entry.assert_called_once_with()
    #     self.date_range.assert_called_once_with(self.last_entry_.date + datetime.timedelta(days=1), self.end)
    #     self.calculate_balances.assert_called_once_with(output, self.last_entry_.balance, self.date_range.return_value)
    #     self.objects.filter.assert_called_with(date__gte=self.start, date__lt=self.end)
    #     self.assertEqual(balances, self.objects.filter().order_by.return_value)

    # def test_not_all_entries_exist_an_no_last_entry(self):
    #     self.len.return_value = 0
    #     last_entry = None
    #     self.last_entry.return_value = last_entry
    #     output = {'columns': ['date', 'balance'], 'values': []}

    #     balances = Balance.get_balances(self.start, self.end)

    #     self.last_entry.assert_called_once_with()
    #     self.date_range.assert_called_once_with(self.start, self.end)
    #     self.calculate_balances.assert_called_once_with(output, 0, self.date_range.return_value)
    #     self.objects.filter.assert_called_with(date__gte=self.start, date__lt=self.end)
    #     self.assertEqual(balances, self.objects.filter().order_by.return_value)
        
