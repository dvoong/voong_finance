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
        return cls.calculate_balances({}, balance, dates)

    @classmethod
    def last_entry(cls):
        return cls.objects.all().order_by('date').last()

    @classmethod
    def calculate_balances(cls, output, initial_balance, dates):
        if len(dates) == 0:
            return output
        initial_balance += Transaction.objects.filter(date=dates[0]).aggregate(Sum('balance'))
        output['values'].append([dates[0].isoformat(), initial_balance])
        return cls.calculate_balances(output, initial_balance, dates[1:])

class Transaction(models.Model):

    type = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    size = models.FloatField(null=True)

class RepeatTransaction(models.Model):
    pass
