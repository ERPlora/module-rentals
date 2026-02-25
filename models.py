from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

RENTAL_STATUS = [
    ('reserved', _('Reserved')),
    ('active', _('Active')),
    ('returned', _('Returned')),
    ('overdue', _('Overdue')),
    ('cancelled', _('Cancelled')),
]

class RentalItem(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=50, blank=True, verbose_name=_('Code'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default='0', verbose_name=_('Daily Rate'))
    is_available = models.BooleanField(default=True, verbose_name=_('Is Available'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    category = models.CharField(max_length=100, blank=True, verbose_name=_('Category'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    quantity_total = models.PositiveIntegerField(default=1, verbose_name=_('Total Quantity'))

    class Meta(HubBaseModel.Meta):
        db_table = 'rentals_rentalitem'

    def __str__(self):
        return self.name


class Rental(HubBaseModel):
    reference = models.CharField(max_length=50, verbose_name=_('Reference'))
    item = models.ForeignKey('RentalItem', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, verbose_name=_('Customer Name'))
    status = models.CharField(max_length=20, default='reserved', choices=RENTAL_STATUS, verbose_name=_('Status'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Total'))
    # Customer link
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('Customer'),
    )
    # Deposit
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default='0', verbose_name=_('Deposit Amount'))
    deposit_paid = models.BooleanField(default=False, verbose_name=_('Deposit Paid'))
    deposit_returned = models.BooleanField(default=False, verbose_name=_('Deposit Returned'))
    # Condition
    condition_out = models.TextField(blank=True, verbose_name=_('Condition at Checkout'))
    condition_in = models.TextField(blank=True, verbose_name=_('Condition at Return'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'rentals_rental'

    def __str__(self):
        return self.reference


class RentalBlackout(HubBaseModel):
    """Dates when a rental item is unavailable (maintenance, reserved, etc.)."""
    item = models.ForeignKey('RentalItem', on_delete=models.CASCADE, related_name='blackouts')
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))
    reason = models.CharField(max_length=255, blank=True, verbose_name=_('Reason'))

    class Meta(HubBaseModel.Meta):
        db_table = 'rentals_blackout'

    def __str__(self):
        return f'{self.item.name}: {self.start_date} - {self.end_date}'

