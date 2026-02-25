from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # RentalItem
    path('rental_items/', views.rental_items_list, name='rental_items_list'),
    path('rental_items/add/', views.rental_item_add, name='rental_item_add'),
    path('rental_items/<uuid:pk>/edit/', views.rental_item_edit, name='rental_item_edit'),
    path('rental_items/<uuid:pk>/delete/', views.rental_item_delete, name='rental_item_delete'),
    path('rental_items/<uuid:pk>/toggle/', views.rental_item_toggle_status, name='rental_item_toggle_status'),
    path('rental_items/bulk/', views.rental_items_bulk_action, name='rental_items_bulk_action'),

    # Rental Item Detail
    path('items/<uuid:pk>/', views.rental_item_detail, name='rental_item_detail'),

    # Blackouts
    path('items/<uuid:pk>/blackouts/add/', views.blackout_add, name='blackout_add'),
    path('items/<uuid:pk>/blackouts/panel/', views.blackout_add_panel, name='blackout_add_panel'),
    path('items/<uuid:pk>/blackouts/<uuid:blackout_pk>/delete/', views.blackout_delete, name='blackout_delete'),

    # Rental
    path('rentals/', views.rentals_list, name='rentals_list'),
    path('rentals/add/', views.rental_add, name='rental_add'),
    path('rentals/<uuid:pk>/edit/', views.rental_edit, name='rental_edit'),
    path('rentals/<uuid:pk>/delete/', views.rental_delete, name='rental_delete'),
    path('rentals/bulk/', views.rentals_bulk_action, name='rentals_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
