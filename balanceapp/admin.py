from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Balance

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'balance', 'income', 'expense')
