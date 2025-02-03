from django.contrib import admin
from .models import Income

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('date', 'purpose', 'amount', 'related_party', 'location')
    search_fields = ('purpose', 'related_party', 'location')
