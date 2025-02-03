from django.contrib import admin
from .models import Expense
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

class ExpenseAdminForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'purpose_details': FilteredSelectMultiple('Purpose Details', is_stacked=False),
        }

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseAdminForm
    list_display = ('date_time', 'purpose', 'amount', 'related_party', 'location')  # Updated field name
    search_fields = ('purpose__name', 'related_party', 'location')
