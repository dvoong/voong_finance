from django import forms

class TransactionForm(forms.Form):

    type = forms.CharField(widget=forms.fields.Select(attrs={'id': 'transaction-type-dropdown'},
                                                                  choices=[(0, 'Income'), (1, 'Expense')]))
    description = forms.CharField(widget=forms.fields.TextInput(attrs={'id': 'transaction-description'}))
    date = forms.CharField(widget=forms.SelectDateWidget(attrs={'id': 'date-selector'}))
    # repeats = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'repeating-transaction-checkbox'}), required=False)
    # frequency = forms.CharField(widget=forms.fields.Select(attrs={'id': 'repeat-frequency-dropdown'},
    #                                                               choices=[(0, 'Monthly')]))
    size = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'transaction-size-input'}))
