from django.db import models

# Create your models here.
class Balance(models.Model):

    date = models.DateField(null=True)
    balance = models.FloatField(null=True)
