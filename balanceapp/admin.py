from django.contrib import admin
from .models import Balance

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'balance', 'income', 'expense')
    ordering = ('date_time',)