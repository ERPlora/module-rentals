from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RentalItem, Rental

class RentalItemForm(forms.ModelForm):
    class Meta:
        model = RentalItem
        fields = ['name', 'code', 'description', 'daily_rate', 'is_available', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'daily_rate': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['reference', 'item', 'customer_name', 'status', 'start_date', 'end_date', 'total', 'notes']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'item': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'customer_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'total': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

