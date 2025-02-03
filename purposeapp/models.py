from django.db import models

class Purpose(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)  # Notes field

    def __str__(self):
        return self.name

class PurposeDetail(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, related_name='details')

    def __str__(self):
        return self.name
