from django.db import models
from balanceapp.models import Balance

class Income(models.Model):
    date = models.DateField()
    purpose = models.CharField(max_length=100)
    purpose_detail = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    related_party = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        super(Income, self).save(*args, **kwargs)
        balance, created = Balance.objects.get_or_create(date=self.date)
        balance.income += self.amount
        balance.balance += self.amount
        balance.save()
