from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'initialise-balance$', views.initialise_balance, name='initialise_balance'),
    url(r'transaction-form$', views.transaction_form, name='transaction_form'),
    url(r'get-balances$', views.get_balances, name='get_balances'),
]
