from django.contrib import admin
from .models import Purpose, PurposeDetail

@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'notes')
    search_fields = ('name',)

@admin.register(PurposeDetail)
class PurposeDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'purpose')
    search_fields = ('name', 'purpose__name')
