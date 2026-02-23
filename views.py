"""
Rental Management Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('rentals', 'dashboard')
@htmx_view('rentals/pages/dashboard.html', 'rentals/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('rentals', 'items')
@htmx_view('rentals/pages/items.html', 'rentals/partials/items_content.html')
def items(request):
    """Items view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('rentals', 'rentals')
@htmx_view('rentals/pages/rentals.html', 'rentals/partials/rentals_content.html')
def rentals(request):
    """Rentals view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('rentals', 'settings')
@htmx_view('rentals/pages/settings.html', 'rentals/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

