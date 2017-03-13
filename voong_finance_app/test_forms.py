from django.test import TestCase
from voong_finance_app.forms import TransactionForm

class TestTransactionForm(TestCase):

    def test(self):

        form = TransactionForm()
        widget = form.fields['type'].widget

        self.assertEqual(widget.attrs['id'], 'transaction-type-dropdown')
        
