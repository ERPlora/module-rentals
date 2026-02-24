from django.contrib import admin

from .models import RentalItem, Rental

@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'daily_rate', 'is_available', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['reference', 'item', 'customer_name', 'status', 'start_date', 'created_at']
    search_fields = ['reference', 'customer_name', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

