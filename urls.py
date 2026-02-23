from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('items/', views.items, name='items'),
    path('rentals/', views.rentals, name='rentals'),
    path('settings/', views.settings, name='settings'),
]
