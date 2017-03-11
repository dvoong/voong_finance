import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from voong_finance_app.forms import TransactionForm

# Create your views here.
def home(request):
    return render(request, 'voong_finance_app/welcome.html')

def initialise_balance(request):
    data = request.POST
    date = data['date'] if 'date' in data else datetime.date.today().isoformat()
    balance = float(request.POST['balance'])
    return JsonResponse({'date': date, 'balance': balance})

def transaction_form(request):
    return render(request, 'voong_finance_app/transaction-form.html', {'form': str(TransactionForm())})
