from django import forms
from django.utils.translation import gettext_lazy as _

from .models import RentalItem, Rental, RentalBlackout

class RentalItemForm(forms.ModelForm):
    class Meta:
        model = RentalItem
        fields = ['name', 'code', 'description', 'daily_rate', 'is_available', 'is_active', 'category', 'location', 'quantity_total']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'daily_rate': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'category': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'location': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'quantity_total': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['reference', 'item', 'customer_name', 'status', 'start_date', 'end_date', 'total', 'customer', 'deposit_amount', 'deposit_paid', 'deposit_returned', 'condition_out', 'condition_in', 'notes']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'item': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'customer_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'total': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'customer': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'deposit_amount': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number', 'step': '0.01'}),
            'deposit_paid': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'deposit_returned': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'condition_out': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 2}),
            'condition_in': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

class RentalBlackoutForm(forms.ModelForm):
    class Meta:
        model = RentalBlackout
        fields = ['item', 'start_date', 'end_date', 'reason']
        widgets = {
            'item': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'start_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'reason': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
        }

