import datetime
from django.db import models

# Create your models here.
class Balance(models.Model):

    date = models.DateField(null=True)
    balance = models.FloatField(null=True)

    @staticmethod
    def recalculate(start, end):
        Balance.objects.filter(date__gte=start).delete()
        transactions = Transaction.objects.filter(date__gte=start, date__lte=end)
        try:
            balance = Balance.objects.get(date=start - datetime.timedelta(days=1)).balance
        except Balance.DoesNotExist as e:
            balance = 0
        Balance.calculate_balance(balance, start, end, transactions)
        # for date in [start + datetime.timedelta(days=i) for i in range((end - start).days + 1)]:
        #     for transaction in transactions.filter(date=date):
        #         balance += transaction.size
        #     Balance.objects.create(date=date, balance=balance)

    # @classmethod
    # def last_entry(cls):
    #     return cls.objects.all().order_by('date').last()

    @classmethod
    def calculate_balance(cls, balance, start, end):
        pass

class Transaction(models.Model):

    type = models.CharField(max_length=30, null=True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    size = models.FloatField(null=True)

class RepeatTransaction(models.Model):
    pass
