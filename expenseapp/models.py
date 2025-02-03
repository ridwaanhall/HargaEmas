from django.db import models
from purposeapp.models import Purpose, PurposeDetail
from balanceapp.models import Balance

class Expense(models.Model):
    date = models.DateField()
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    purpose_details = models.ManyToManyField(PurposeDetail, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    related_party = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        super(Expense, self).save(*args, **kwargs)
        balance, created = Balance.objects.get_or_create(date=self.date)
        balance.expense += self.amount
        balance.balance -= self.amount
        balance.save()

    @property
    def notes(self):
        return self.purpose.notes
