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
        balances = cls.objects.filter(date__gte=start, date__lt=end)#.order_by('date')
        if len(balances) == (end - start).days:
            return balances
        last_entry = cls.last_entry()
        missing_dates = cls.find_missing_dates(date_range(start, end), balances)
            
        # if len(missing_dates) == 0:
        #     return balances
        # else:
        #     entry = balances.first()
        #     if entry:
        #         # if a blance objects exists in this range, calculate balances before and after them
        #         dates = date_range(start, entry.date)
        #         output = {'columns': ['date', 'balance'], 'values': []}
        #         cls.calculate_balances(output, 0, dates)

        #         entry = balances.last()
        #         dates = date_range(entry.date + datetime.timedelta(days=1), end)
        #         output = {'columns': ['date', 'balance'], 'values': []}
        #         cls.calculate_balances(output, entry.balance, dates)
        #     else: # look back for the last entry
        #         last_entry = cls.last_entry()
        #         if last_entry == None:
        #             output = {'columns': ['date', 'balance'], 'values': []}
        #             cls.calculate_balances(output, 0, date_range(start, end))
        #         elif last_entry < start:
        #             output = {'columns': ['date', 'balance'], 'values': []}
        #             dates = date_range(last_entry.date + datetime.timedelta(days=1), end)
        #             cls.calculate_balances(output, last_entry.balance, dates)
        #         else:
        #             first_entry = cls.first_entry()
        #             output = {'columns': ['date', 'balance'], 'values': []}
        #             dates = date_range(start, first_entry.date)
        #             cls.calculate_balances(output, 0, dates)
            
        # output = cls.objects.filter(date__gte=start, date__lt=end).order_by('date')
        # return output

    @staticmethod
    def find_missing_dates(cls, dates, balances):
        # missing_dates = filter(lambda date: len(balances.filter(date=date)) == 0, date_range(start, end))
        pass
        

class Transaction(models.Model):

    type = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    size = models.FloatField(null=True)

class RepeatTransaction(models.Model):
    pass
