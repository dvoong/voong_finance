import json
import datetime
from django.db import models
from django.db.models import Sum
from voong_finance_app.utils import date_range

# Create your models here.
class Balance(models.Model):

    date = models.DateField(null=True)
    balance = models.FloatField(null=True)

    @classmethod
    def recalculate(cls, start, end):
        cls.objects.filter(date__gte=start).delete()
        dates = date_range(start, end)
        last_entry = Balance.last_entry()
        balance = last_entry.balance if last_entry != None else 0
        output = cls.calculate_balances({'columns': ['date', 'balance'], 'values': []}, balance, dates)
        return output

    @classmethod
    def last_entry(cls):
        return cls.objects.all().order_by('date').last()

    @classmethod
    def calculate_balances(cls, output, initial_balance, dates):
        if len(dates) == 0:
            return output
        transactions = Transaction.objects.filter(date=dates[0])
        if len(transactions):
            initial_balance += transactions.aggregate(Sum('size'))['size__sum']
        cls.objects.create(date=dates[0], balance=initial_balance)
        output['values'].append([dates[0].isoformat(), initial_balance])
        return cls.calculate_balances(output, initial_balance, dates[1:])

    @staticmethod
    def to_dict(balances):
        output = {'columns': ['date', 'balance']}
        output['values'] = list(map(lambda e: [e.date.isoformat(), e.balance], balances))
        return output

    @classmethod
    def get_balances(cls, start, end):
        balances = cls.objects.filter(date__gte=start, date__lt=end).order_by('date')
        dates = set(map(lambda x: x.date, balances))
        if len(dates) == (end - start).days:
            return balances
        else:
            # last_entry = cls.last_entry() # get last entry before start
            previous_entries = cls.objects.filter(date__lt=start).order_by('date')
            last_entry = previous_entries[len(previous_entries) - 1] if len(previous_entries) else None
            balance = last_entry.balance if last_entry else 0
            missing_dates = list(set(date_range(start, end)) - dates) # only dates that don't have a balance already
            output = {'columns': ['date', 'balance'], 'values': []}
            cls.calculate_balances(output, balance, missing_dates)
        output = cls.objects.filter(date__gte=start, date__lt=end).order_by('date')
        return output
        

class Transaction(models.Model):

    type = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    size = models.FloatField(null=True)

class RepeatTransaction(models.Model):
    pass
