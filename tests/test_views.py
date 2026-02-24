"""Tests for rentals views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('rentals:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('rentals:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('rentals:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestRentalItemViews:
    """RentalItem view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('rentals:rental_items_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('rentals:rental_item_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('rentals:rental_item_add')
        data = {
            'name': 'New Name',
            'code': 'New Code',
            'description': 'Test description',
            'daily_rate': '100.00',
            'is_available': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, rental_item):
        """Test edit form loads."""
        url = reverse('rentals:rental_item_edit', args=[rental_item.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, rental_item):
        """Test editing via POST."""
        url = reverse('rentals:rental_item_edit', args=[rental_item.pk])
        data = {
            'name': 'Updated Name',
            'code': 'Updated Code',
            'description': 'Test description',
            'daily_rate': '100.00',
            'is_available': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, rental_item):
        """Test soft delete via POST."""
        url = reverse('rentals:rental_item_delete', args=[rental_item.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        rental_item.refresh_from_db()
        assert rental_item.is_deleted is True

    def test_toggle_status(self, auth_client, rental_item):
        """Test toggle active status."""
        url = reverse('rentals:rental_item_toggle_status', args=[rental_item.pk])
        original = rental_item.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        rental_item.refresh_from_db()
        assert rental_item.is_active != original

    def test_bulk_delete(self, auth_client, rental_item):
        """Test bulk delete."""
        url = reverse('rentals:rental_items_bulk_action')
        response = auth_client.post(url, {'ids': str(rental_item.pk), 'action': 'delete'})
        assert response.status_code == 200
        rental_item.refresh_from_db()
        assert rental_item.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('rentals:rental_items_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestRentalViews:
    """Rental view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('rentals:rentals_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('rentals:rental_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('rentals:rental_add')
        data = {
            'reference': 'New Reference',
            'customer_name': 'New Customer Name',
            'status': 'New Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, rental):
        """Test edit form loads."""
        url = reverse('rentals:rental_edit', args=[rental.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, rental):
        """Test editing via POST."""
        url = reverse('rentals:rental_edit', args=[rental.pk])
        data = {
            'reference': 'Updated Reference',
            'customer_name': 'Updated Customer Name',
            'status': 'Updated Status',
            'start_date': '2025-01-15',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, rental):
        """Test soft delete via POST."""
        url = reverse('rentals:rental_delete', args=[rental.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        rental.refresh_from_db()
        assert rental.is_deleted is True

    def test_bulk_delete(self, auth_client, rental):
        """Test bulk delete."""
        url = reverse('rentals:rentals_bulk_action')
        response = auth_client.post(url, {'ids': str(rental.pk), 'action': 'delete'})
        assert response.status_code == 200
        rental.refresh_from_db()
        assert rental.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('rentals:rentals_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('rentals:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('rentals:settings')
        response = client.get(url)
        assert response.status_code == 302

