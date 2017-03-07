from django import forms

class TransactionForm(forms.Form):

    transaction_type = forms.CharField(widget=forms.fields.Select(attrs={'id': 'transaction-type-dropdown'},
                                                                  choices=[(0, 'Expense')]))
    transaction_description = forms.CharField(widget=forms.fields.TextInput(attrs={'id': 'transaction-description'}))
    date = forms.CharField(widget=forms.SelectDateWidget(attrs={'id': 'date-selector'}))
    # date = forms.CharField(widget=forms.DateInput(attrs={'id': 'date-selector'}))
