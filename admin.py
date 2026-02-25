from django.contrib import admin

from .models import RentalItem, Rental, RentalBlackout

@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'daily_rate', 'is_available', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['reference', 'item', 'customer_name', 'status', 'start_date', 'deposit_amount', 'deposit_paid', 'created_at']
    search_fields = ['reference', 'customer_name', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RentalBlackout)
class RentalBlackoutAdmin(admin.ModelAdmin):
    list_display = ['item', 'start_date', 'end_date', 'reason', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

