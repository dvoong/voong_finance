import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from voong_finance_app.forms import TransactionForm
from voong_finance_app.models import Balance

# Create your views here.
def home(request):
    return render(request, 'voong_finance_app/welcome.html')

def initialise_balance(request):
    data = request.POST
    if 'date' in data and data['date'] != '':
        date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
    else:
        date = datetime.date.today()
    date_str = date.isoformat()
    balance = float(request.POST['balance'])
    for i in range(28):
        Balance.objects.create(date=date + datetime.timedelta(days=i), balance=balance)
    output = {
        'columns': ['date', 'balance'],
        'values': [(balance.date.isoformat(), balance.balance) for balance in Balance.objects.all().order_by('date')]
    }
    return JsonResponse(output)
    return JsonResponse({'date': date_str, 'balance': balance})

def transaction_form(request):
    return render(request, 'voong_finance_app/transaction-form.html', {'form': str(TransactionForm())})
