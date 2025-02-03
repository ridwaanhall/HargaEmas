from django.db import models
from purposeapp.models import Purpose, PurposeDetail
from balanceapp.models import Balance
from locationapp.models import Location, RelatedParty
from paymentapp.models import PaymentMethod, PaymentStatus
from django.utils import timezone

class Income(models.Model):
    date_time = models.DateTimeField(default=timezone.now)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    purpose_details = models.ManyToManyField(PurposeDetail, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Reference Location
    related_parties = models.ManyToManyField(RelatedParty, blank=True)  # Updated to use ManyToManyField
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Income, self).save(*args, **kwargs)
        balance, created = Balance.objects.get_or_create(date_time=self.date_time)
        balance.income += self.amount
        balance.balance += self.amount
        balance.save()
