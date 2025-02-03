from django.contrib import admin
from .models import Income
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

class IncomeAdminForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'
        widgets = {
            'purpose_details': FilteredSelectMultiple('Purpose Details', is_stacked=False),
        }

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    form = IncomeAdminForm
    list_display = ('date_time', 'purpose', 'amount', 'related_party', 'location')  # Updated field name
    search_fields = ('purpose__name', 'related_party', 'location')
