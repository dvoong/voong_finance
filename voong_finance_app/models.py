from django.contrib.auth.models import User

# from django.db import models

# class User(models.Model):

#     email = models.EmailField()
#     password = models.CharField(max_length=100)

# import json
# import datetime
# from django.db import models
# from django.db.models import Sum
# from voong_finance_app.utils import date_range

# # Create your models here.
# class Balance(models.Model):

#     date = models.DateField(null=True)
#     balance = models.FloatField(null=True)

#     @classmethod
#     def recalculate(cls, start, end):
#         cls.objects.filter(date__gte=start).delete()
#         return cls.get_balances(start, end)

#     @classmethod
#     def last_entry(cls):
#         return cls.objects.all().order_by('date').last()

#     @classmethod
#     def calculate_balances(cls, dates, starting_balance):
#         if len(dates) == 0:
#             return []
#         transactions = Transaction.objects.filter(date=dates[0])
#         if len(transactions) > 0:
#             starting_balance += transactions.aggregate(Sum('size'))['size__sum']
#         return [cls.objects.create(date=dates[0], balance=starting_balance)] + cls.calculate_balances(dates[1:], starting_balance)
            
#     @staticmethod
#     def to_dict(balances):
#         output = {'columns': ['date', 'balance']}
#         output['values'] = list(map(lambda e: [e.date.isoformat(), e.balance], balances))
#         return output

#     @classmethod
#     def get_balances(cls, start, end):
#         balances = cls.objects.filter(date__gte=start, date__lt=end).order_by('date')
#         if len(balances) == (end - start).days:
#             return balances
#         last_entry = cls.last_entry()
#         if last_entry == None:
#             balances = cls.calculate_balances(dates=date_range(start, end), starting_balance=0)
#             return balances
#         else:
#             dates = date_range(last_entry.date + datetime.timedelta(days=1), end)
#             after = cls.calculate_balances(dates=dates, starting_balance=last_entry.balance)
#             first_entry = Balance.objects.first()
#             before = cls.calculate_balances(dates=date_range(start, first_entry.date), starting_balance=0)
#             return before + list(balances) + after

# class Transaction(models.Model):

#     type = models.CharField(max_length=30, null=True)
#     description = models.CharField(max_length=200, null=True)
#     date = models.DateField(null=True)
#     size = models.FloatField(null=True)

# class RepeatTransaction(models.Model):
#     pass
