from django import forms

class TransactionForm(forms.Form):

    transaction_type = forms.CharField(widget=forms.fields.Select(attrs={'id': 'transaction-type-dropdown'},
                                                                  choices=[(0, 'Expense')]))
    transaction_description = forms.CharField(widget=forms.fields.TextInput(attrs={'id': 'transaction-description'}))
    date = forms.CharField(widget=forms.SelectDateWidget(attrs={'id': 'date-selector'}))
    repeat_transaction = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'repeating-transaction-checkbox'}))
    repeat_frequency = forms.CharField(widget=forms.fields.Select(attrs={'id': 'repeat-frequency-dropdown'},
                                                                  choices=[(0, 'Monthly')]))
    transaction_size = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'transaction-size-input'}))
