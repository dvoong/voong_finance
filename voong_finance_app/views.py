from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'voong_finance_app/welcome.html')

def initialise_balance(request):
    return JsonResponse({'date': None, 'balance': float(request.POST['balance'])})
