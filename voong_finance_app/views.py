from django.shortcuts import render, redirect
from django.http import HttpResponse

def welcome(request):
    return render(request, 'voong_finance_app/welcome.html')

def registration(request):
    return render(request, 'voong_finance_app/registration.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'voong_finance_app/signin.html')
    elif request.method == 'POST':
        return redirect('/')

# import datetime
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from voong_finance_app.forms import TransactionForm
# from voong_finance_app.models import Balance, Transaction, RepeatTransaction
# from voong_finance_app.utils import convert_date_string, get_month_dates
#
# # Create your views here.
# def home(request):
#     dates = get_month_dates(datetime.date.today())
#     if len(Balance.objects.all()):
#         return render(request, 'voong_finance_app/home.html', {'dates': dates})
#     return render(request, 'voong_finance_app/welcome.html', {'dates': dates})
#
# def initialise_balance(request):
#     data = request.POST
#     if 'date' in data and data['date'] != '':
#         date = convert_date_string(data['date'])
#     else:
#         date = datetime.date.today()
#
#     Transaction.objects.create(type='Initialisation', description='Initialisation', date=date, size=float(request.POST['balance']))
#     balances = Balance.get_balances(start=date, end=date + datetime.timedelta(days=28))
#     return JsonResponse(Balance.to_dict(balances))
#
# def transaction_form(request):
#     if request.method == 'GET':
#         return render(request, 'voong_finance_app/transaction-form.html', {'form': str(TransactionForm(initial={'date': datetime.date.today()}))})
#     elif request.method == 'POST':
#         year = int(request.POST['date_year'])
#         month = int(request.POST['date_month'])
#         day = int(request.POST['date_day'])
#         date = datetime.date(year, month, day)
#         transaction_type = int(request.POST['type'])
#         size = abs(float(request.POST['size']))
#         if transaction_type == 1:
#             size *= -1
#
#         transaction = Transaction.objects.create(date=date,
#                                                  description=request.POST['description'],
#                                                  type=transaction_type,
#                                                  size=size)
#
#         for t in Transaction.objects.all():
#             print('{}: {}, {}, {}'.format(t.date, t.type, t.description, t.size))
#         # untested
#         start = convert_date_string(request.POST['chart_date_start'])
#         end = convert_date_string(request.POST['chart_date_end']) + datetime.timedelta(days=1)
#         balances = Balance.recalculate(date, end)
#         ##
#
#         return JsonResponse(Balance.to_dict(balances))
#
# def get_balances(request):
#     today = datetime.date.today()
#     start = today - datetime.timedelta(days=13)
#     end = today + datetime.timedelta(days=15)
#     balances = Balance.get_balances(start=start, end=end)
#     dict_ = Balance.to_dict(balances)
#     response = JsonResponse(dict_)
#     return response
