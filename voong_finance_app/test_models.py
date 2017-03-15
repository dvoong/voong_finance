import datetime
from unittest import mock
from django.test import TestCase
from voong_finance_app.models import Transaction, Balance

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

        self.calculate_balances.assert_called_once_with({}, self.last_entry.return_value.balance, self.date_range.return_value)

    def test_if_last_entry_does_not_exist_call_calulate_balances_with_its_balance(self):
        self.last_entry.return_value = None

        balances = Balance.recalculate(self.start, self.end)

        self.calculate_balances.assert_called_once_with({}, 0, self.date_range.return_value)

        
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
        

class TestBalanceCalculateBalances(TestCase):

    # if the number of dates is 0 then return the output
    # calculate_the_balance_for_the_first_date
    # add the balance to the output
    # calls calculate_balance for the remaning dates

    def setUp(self):
        self.Transaction_patch = mock.patch('voong_finance_app.models.Transaction')
        self.Transaction = self.Transaction_patch.start()
        self.Sum_patch = mock.patch('voong_finance_app.models.Sum')
        self.Sum = self.Sum_patch.start()

    def tearDown(self):
        self.Transaction.stop()
        self.Sum.stop()

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
        
        output = Balance.calculate_balances(input, initial_balance, dates)

        self.Transaction.objects.filter.assert_called_with(date=dates[1])
        self.assertEqual(self.Transaction.objects.filter.call_count, 2)
        self.Transaction.objects.filter.return_value.aggregate.assert_called_with(self.Sum.return_value)
        self.Sum.assert_called_with('balance')

    def test_add_the_balance_to_the_output(self):

        input = {'columns': ['date', 'balance'], 'values': [['2017-02-28', 7]]}
        initial_balance = 7
        dates = [datetime.date(2017, 3, 1)]
        self.Transaction.objects.filter.return_value.aggregate.return_value = -4
        
        output = Balance.calculate_balances(input, initial_balance, dates)

        self.assertEqual(output['values'][1][0], '2017-03-01')
        self.assertEqual(output['values'][1][1], 3)

    
