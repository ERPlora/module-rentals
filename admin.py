from django.contrib import admin

from .models import RentalItem, Rental

@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description', 'daily_rate', 'is_available']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['reference', 'item', 'customer_name', 'status', 'start_date']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

