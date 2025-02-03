from django.db import models

class Location(models.Model):
    location_name = models.CharField(max_length=100, default='None')
    location_link = models.URLField(blank=True, null=True)  # Link can be blank and null

    def __str__(self):
        return self.location_name

class RelatedParty(models.Model):
    name = models.CharField(max_length=100)  # Name of the related party

    def __str__(self):
        return self.name
