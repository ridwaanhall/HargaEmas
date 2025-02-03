from django.db import models
from django.utils import timezone

class Balance(models.Model):
    date_time = models.DateTimeField(default=timezone.now)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
