    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'rentals'
    MODULE_NAME = _('Rental Management')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'key-outline'
    MODULE_DESCRIPTION = _('Equipment, vehicle and space rental management')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'services'

    MENU = {
        'label': _('Rental Management'),
        'icon': 'key-outline',
        'order': 36,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Items'), 'icon': 'cube-outline', 'id': 'items'},
{'label': _('Rentals'), 'icon': 'key-outline', 'id': 'rentals'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'rentals.view_rental',
'rentals.add_rental',
'rentals.change_rental',
'rentals.delete_rental',
'rentals.view_rentalitem',
'rentals.add_rentalitem',
'rentals.change_rentalitem',
'rentals.manage_settings',
    ]
