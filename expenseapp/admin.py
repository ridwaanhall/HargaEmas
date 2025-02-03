from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'purpose', 'amount', 'related_party', 'location')
    search_fields = ('purpose', 'related_party', 'location')
