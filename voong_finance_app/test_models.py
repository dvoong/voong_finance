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

    def tearDown(self):
        self.get_patch.stop()
        
    def test_deletes_existing_balance_entries_equal_to_and_greater_than_start(self):

        Balance.recalculate(self.start, self.end)
        
        self.filtered.delete.assert_called_once_with()

    def test_filteres_balance_entries_equal_to_and_greater_than_start(self):

        Balance.recalculate(self.start, self.end)

        Balance.objects.filter.assert_called_once_with(date__gte=self.start)

    def test_gets_all_transactions_with_date_gte_start(self):
        TransactionPatch = mock.patch('voong_finance_app.models.Transaction')
        Transaction = TransactionPatch.start()
        transactions = mock.Mock()
        Transaction.objects.filter = mock.Mock(return_value=transactions)

        Balance.recalculate(self.start, self.end)

        Transaction.objects.filter.assert_called_once_with(date__gte=self.start, date__lte=self.end)
        
        TransactionPatch.stop()
        
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
        
