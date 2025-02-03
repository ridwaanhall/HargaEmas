from django.contrib import admin
from .models import Location, RelatedParty

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_link')
    search_fields = ('location_name',)

@admin.register(RelatedParty)
class RelatedPartyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  # Completed the search field definition
