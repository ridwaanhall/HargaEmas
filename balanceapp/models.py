from django.db import models

class Balance(models.Model):
    date = models.DateField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
