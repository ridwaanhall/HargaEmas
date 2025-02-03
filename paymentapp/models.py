from django.db import models

class PaymentMethod(models.Model):
    payment_name = models.CharField(max_length=100, default='Not Specified')

    def __str__(self):
        return self.payment_name

class PaymentStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status
