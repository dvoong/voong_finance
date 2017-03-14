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

class TestBalance(TestCase):
    def setUp(self):
        self.start = datetime.date(2017, 1, 24)
        self.end = datetime.date(2017, 1, 31)
        self.filtered = mock.Mock()
        Balance.objects.filter = mock.Mock(return_value=self.filtered)
        self.get_patch = mock.patch('voong_finance_app.models.Balance.objects.get')
        self.get = self.get_patch.start()
        self.calculate_balance_patch = mock.patch('voong_finance_app.models.Balance.calculate_balance')
        self.calculate_balance = self.calculate_balance_patch.start()
        self.TransactionPatch = mock.patch('voong_finance_app.models.Transaction')
        self.Transaction = self.TransactionPatch.start()
        self.transactions = mock.Mock()
        self.Transaction.objects.filter = mock.Mock(return_value=self.transactions)
        
    def tearDown(self):
        self.get_patch.stop()
        self.calculate_balance_patch.stop()
        self.TransactionPatch.stop()
        
    def test_deletes_existing_balance_entries_equal_to_and_greater_than_start(self):

        Balance.recalculate(self.start, self.end)
        
        self.filtered.delete.assert_called_once_with()

    def test_filteres_balance_entries_equal_to_and_greater_than_start(self):

        Balance.recalculate(self.start, self.end)

        Balance.objects.filter.assert_called_once_with(date__gte=self.start)

    def test_gets_all_transactions_with_date_gte_start(self):

        Balance.recalculate(self.start, self.end)

        self.Transaction.objects.filter.assert_called_once_with(date__gte=self.start, date__lte=self.end)
        
    # def test_creates_balance_entry_for_each_date(self):

    #     Balance.recalculate(self.start, self.end)

    #     Balance.objects.create.call_count = 8
    #     Balance.objects.create.call_args_list[0][1] = {'date': datetime.date(2017, 1, 24), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[1][1] = {'date': datetime.date(2017, 1, 25), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[2][1] = {'date': datetime.date(2017, 1, 26), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[3][1] = {'date': datetime.date(2017, 1, 27), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[4][1] = {'date': datetime.date(2017, 1, 28), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[5][1] = {'date': datetime.date(2017, 1, 29), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[6][1] = {'date': datetime.date(2017, 1, 30), 'balance': last_balance}
    #     Balance.objects.create.call_args_list[7][1] = {'date': datetime.date(2017, 1, 31), 'balance': last_balance}

    def test_gets_balance_on_day_before_start(self):
        
        Balance.recalculate(self.start, self.end)

        self.get.assert_called_once_with(date=datetime.date(2017, 1, 23))
        
    def test_if_get_raises_DoesNotExist_error_then_calculate_balance_with_an_initial_balance_of_0(self):
        self.get.side_effect = Balance.DoesNotExist

        Balance.recalculate(self.start, self.end)

        self.calculate_balance.assert_called_once_with(0, self.start, self.end, self.transactions)


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
                                        balance=10)
        
        last_entry = Balance.last_entry()
    
        self.assertEqual(entry2, last_entry)

    def test_when_there_are_no_balance_entries_return_none(self):
        last_entry = Balance.last_entry()

        self.assertEqual(None, last_entry)
        
