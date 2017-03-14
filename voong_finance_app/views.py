import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from voong_finance_app.forms import TransactionForm
from voong_finance_app.models import Balance, Transaction, RepeatTransaction

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
    if request.method == 'GET':
        return render(request, 'voong_finance_app/transaction-form.html', {'form': str(TransactionForm())})
    elif request.method == 'POST':
        year = int(request.POST['date_year'])
        month = int(request.POST['date_month'])
        day = int(request.POST['date_day'])
        date = datetime.date(year, month, day)
        if 'repeats' not in request.POST:
            Transaction.objects.create(date=date,
                                       description=request.POST['description'],
                                       type=request.POST['type'],
                                       size=float(request.POST['size']))
        else:
            year = request.POST['end_date_year']
            month = request.POST['end_date_month']
            day = request.POST['end_date_day']
            end_date = datetime.date(year, month, day)
            transaction = RepeatTransaction(description=request.POST['description'],
                                            date=date,
                                            frequency=request.POST['frequency'],
                                            size=request.POST['size'],
                                            type=request.POST['type'],
                                            end_date=end_date)

            transaction.create_transactions(transaction.date, Balance.last_entry().date)

        last_entry = Balance.last_entry()
        end = last_entry.date if last_entry else datetime.date.today() + datetime.timedelta(days=28)
        Balance.recalculate(date, end)
        return JsonResponse({'status': 200})
