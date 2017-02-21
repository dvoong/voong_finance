from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'voong_finance_app/welcome.html')

def initialise_balance(request):
    pass
