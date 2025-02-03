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
            'related_parties': FilteredSelectMultiple('Related Parties', is_stacked=False),
        }

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    form = IncomeAdminForm
    list_display = ('date_time', 'purpose', 'amount', 'location')
    search_fields = ('purpose__name', 'location__location_name')

    # Define fieldsets to create sections in the admin form
    fieldsets = (
        ('Common Information', {
            'fields': ('date_time', 'purpose', 'purpose_details')
        }),
        ('Financial Information', {
            'fields': ('amount', 'payment_method', 'payment_status')
        }),
        ('Location and Related Parties', {
            'fields': ('location', 'related_parties')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
