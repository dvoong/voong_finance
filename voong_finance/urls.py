"""voong_finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from voong_finance_app import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'registration', views.registration, name='registration'),
    url(r'signin', views.signin, name='signin'),
    url(r'home', views.home, name='home'),
    url(r'create-transaction', views.create_transaction, name='create-transaction'),
    url(r'get-transactions', views.get_transactions, name='get-transactions'),
    url(r'^app/', include('voong_finance_app.urls')),
    url(r'^api/', include('voong_finance_app.urls')),
    url(r'^admin/', admin.site.urls),
]
