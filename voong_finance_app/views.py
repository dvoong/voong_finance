import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from voong_finance_app.models import User, Transaction
from django.contrib.auth import authenticate, login
from django.core import serializers

def welcome(request):
    return render(request, 'voong_finance_app/welcome.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'voong_finance_app/home.html', context={'today': datetime.date.today().isoformat()})
    else:
        return redirect('/signin')

def registration(request):
    
    if request.method == 'GET':
        return render(request, 'voong_finance_app/registration.html')
        
    elif request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=email)
        return redirect('/signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'voong_finance_app/signin.html')
    elif request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/home')
        else:
            return

def create_transaction(request):
    user = request.user
    date = request.POST['date']
    transaction_type = request.POST['transaction-type']
    description = request.POST['description']
    transaction_size = float(request.POST['transaction-size'])

    previous_transaction = Transaction.objects.filter(user=user, date__lte=date).order_by('-date', '-ordinal')[:1]
    previous_transaction = previous_transaction[0] if len(previous_transaction) > 0 else None
    start_balance = previous_transaction.balance if previous_transaction else 0
    transaction_size = transaction_size if transaction_type == 'income' else -1 * transaction_size
    end_balance = start_balance + float(transaction_size)
    ordinal = len(Transaction.objects.filter(user=user, date=date))

    transaction = Transaction.objects.create(
        user=user,
        date=date,
        type=transaction_type,
        description=description,
        size=transaction_size,
        balance=end_balance,
        ordinal=ordinal
    )

    transaction.refresh_from_db()

    later_transactions = Transaction.objects.filter(user=user, date__gte=date).order_by('date', 'ordinal')
    for t in later_transactions:
        if t.date == transaction.date and t.ordinal <= transaction.ordinal:
            continue
        end_balance += t.size
        t.balance = end_balance
        t.save()
    
    return JsonResponse({
        'date': transaction.date,
        'transaction_type': transaction.type,
        'description': transaction.description,
        'transaction_size': transaction.size,
        'balance': transaction.balance,
        'ordinal': transaction.ordinal
    })

def get_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('date', 'ordinal')
    transactions_json = []
    for t in transactions:
        transactions_json.append({
            'date': t.date,
            'transaction_type': t.type,
            'description': t.description,
            'transaction_size': t.size,
            'balance': t.balance,
            'ordinal': t.ordinal
        })
    return JsonResponse({
        'data': transactions_json,
        'status': 200
    })
