"""
Rental Management Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import RentalItem, Rental, RentalBlackout

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('rentals', 'dashboard')
@htmx_view('rentals/pages/index.html', 'rentals/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_rental_items': RentalItem.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_rentals': Rental.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# RentalItem
# ======================================================================

RENTAL_ITEM_SORT_FIELDS = {
    'code': 'code',
    'name': 'name',
    'is_available': 'is_available',
    'is_active': 'is_active',
    'daily_rate': 'daily_rate',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_rental_items_context(hub_id, per_page=10):
    qs = RentalItem.objects.filter(hub_id=hub_id, is_deleted=False).order_by('code')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'rental_items': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'code',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_rental_items_list(request, hub_id, per_page=10):
    ctx = _build_rental_items_context(hub_id, per_page)
    return django_render(request, 'rentals/partials/rental_items_list.html', ctx)

@login_required
@with_module_nav('rentals', 'items')
@htmx_view('rentals/pages/rental_items.html', 'rentals/partials/rental_items_content.html')
def rental_items_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'code')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = RentalItem.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(description__icontains=search_query))

    order_by = RENTAL_ITEM_SORT_FIELDS.get(sort_field, 'code')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['code', 'name', 'is_available', 'is_active', 'daily_rate', 'description']
        headers = ['Code', 'Name', 'Is Available', 'Is Active', 'Daily Rate', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='rental_items.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='rental_items.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'rentals/partials/rental_items_list.html', {
            'rental_items': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'rental_items': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def rental_item_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip()
        description = request.POST.get('description', '').strip()
        daily_rate = request.POST.get('daily_rate', '0') or '0'
        is_available = request.POST.get('is_available') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        obj = RentalItem(hub_id=hub_id)
        obj.name = name
        obj.code = code
        obj.description = description
        obj.daily_rate = daily_rate
        obj.is_available = is_available
        obj.is_active = is_active
        obj.save()
        return _render_rental_items_list(request, hub_id)
    return django_render(request, 'rentals/partials/panel_rental_item_add.html', {})

@login_required
def rental_item_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.code = request.POST.get('code', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.daily_rate = request.POST.get('daily_rate', '0') or '0'
        obj.is_available = request.POST.get('is_available') == 'on'
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_rental_items_list(request, hub_id)
    return django_render(request, 'rentals/partials/panel_rental_item_edit.html', {'obj': obj})

@login_required
@require_POST
def rental_item_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_rental_items_list(request, hub_id)

@login_required
@require_POST
def rental_item_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_rental_items_list(request, hub_id)

@login_required
@require_POST
def rental_items_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = RentalItem.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_rental_items_list(request, hub_id)


# ======================================================================
# Rental
# ======================================================================

RENTAL_SORT_FIELDS = {
    'reference': 'reference',
    'item': 'item',
    'status': 'status',
    'total': 'total',
    'customer_name': 'customer_name',
    'start_date': 'start_date',
    'created_at': 'created_at',
}

def _build_rentals_context(hub_id, per_page=10):
    qs = Rental.objects.filter(hub_id=hub_id, is_deleted=False).order_by('reference')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'rentals': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'reference',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_rentals_list(request, hub_id, per_page=10):
    ctx = _build_rentals_context(hub_id, per_page)
    return django_render(request, 'rentals/partials/rentals_list.html', ctx)

@login_required
@with_module_nav('rentals', 'rentals')
@htmx_view('rentals/pages/rentals.html', 'rentals/partials/rentals_content.html')
def rentals_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'reference')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Rental.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(reference__icontains=search_query) | Q(customer_name__icontains=search_query) | Q(status__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = RENTAL_SORT_FIELDS.get(sort_field, 'reference')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['reference', 'item', 'status', 'total', 'customer_name', 'start_date']
        headers = ['Reference', 'RentalItem', 'Status', 'Total', 'Customer Name', 'Start Date']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='rentals.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='rentals.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'rentals/partials/rentals_list.html', {
            'rentals': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'rentals': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def rental_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        reference = request.POST.get('reference', '').strip()
        customer_name = request.POST.get('customer_name', '').strip()
        status = request.POST.get('status', '').strip()
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        total = request.POST.get('total', '0') or '0'
        notes = request.POST.get('notes', '').strip()
        obj = Rental(hub_id=hub_id)
        obj.reference = reference
        obj.customer_name = customer_name
        obj.status = status
        obj.start_date = start_date
        obj.end_date = end_date
        obj.total = total
        obj.notes = notes
        obj.save()
        return _render_rentals_list(request, hub_id)
    return django_render(request, 'rentals/partials/panel_rental_add.html', {})

@login_required
def rental_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Rental, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.reference = request.POST.get('reference', '').strip()
        obj.customer_name = request.POST.get('customer_name', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.start_date = request.POST.get('start_date') or None
        obj.end_date = request.POST.get('end_date') or None
        obj.total = request.POST.get('total', '0') or '0'
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_rentals_list(request, hub_id)
    return django_render(request, 'rentals/partials/panel_rental_edit.html', {'obj': obj})

@login_required
@require_POST
def rental_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Rental, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_rentals_list(request, hub_id)

@login_required
@require_POST
def rentals_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Rental.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_rentals_list(request, hub_id)


# ======================================================================
# Rental Item Detail + Blackouts
# ======================================================================

@login_required
@with_module_nav('rentals', 'items')
@htmx_view('rentals/pages/rental_item_detail.html', 'rentals/partials/rental_item_detail_content.html')
def rental_item_detail(request, pk):
    hub_id = request.session.get('hub_id')
    item = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    return {
        'item': item,
        'blackouts': RentalBlackout.objects.filter(item=item, is_deleted=False).order_by('-start_date'),
        'active_rentals': Rental.objects.filter(item=item, is_deleted=False, status__in=['active', 'reserved']).order_by('-start_date')[:10],
    }


def _render_blackouts_list(request, item):
    blackouts = RentalBlackout.objects.filter(item=item, is_deleted=False).order_by('-start_date')
    return django_render(request, 'rentals/partials/blackouts_list.html', {
        'item': item,
        'blackouts': blackouts,
    })


@login_required
@require_POST
def blackout_add(request, pk):
    hub_id = request.session.get('hub_id')
    item = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    blackout = RentalBlackout(hub_id=hub_id)
    blackout.item = item
    blackout.start_date = request.POST.get('start_date') or None
    blackout.end_date = request.POST.get('end_date') or None
    blackout.reason = request.POST.get('reason', '').strip()
    blackout.save()
    return _render_blackouts_list(request, item)


@login_required
@require_POST
def blackout_delete(request, pk, blackout_pk):
    hub_id = request.session.get('hub_id')
    item = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    blackout = get_object_or_404(RentalBlackout, pk=blackout_pk, item=item, is_deleted=False)
    blackout.is_deleted = True
    blackout.deleted_at = timezone.now()
    blackout.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_blackouts_list(request, item)


@login_required
def blackout_add_panel(request, pk):
    hub_id = request.session.get('hub_id')
    item = get_object_or_404(RentalItem, pk=pk, hub_id=hub_id, is_deleted=False)
    return django_render(request, 'rentals/partials/panel_blackout_add.html', {'item': item})


@login_required
@with_module_nav('rentals', 'settings')
@htmx_view('rentals/pages/settings.html', 'rentals/partials/settings_content.html')
def settings_view(request):
    return {}

