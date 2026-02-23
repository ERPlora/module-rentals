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
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'rentals_rental'

    def __str__(self):
        return self.reference

