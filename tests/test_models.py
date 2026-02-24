"""Tests for rentals models."""
import pytest
from django.utils import timezone

from rentals.models import RentalItem, Rental


@pytest.mark.django_db
class TestRentalItem:
    """RentalItem model tests."""

    def test_create(self, rental_item):
        """Test RentalItem creation."""
        assert rental_item.pk is not None
        assert rental_item.is_deleted is False

    def test_str(self, rental_item):
        """Test string representation."""
        assert str(rental_item) is not None
        assert len(str(rental_item)) > 0

    def test_soft_delete(self, rental_item):
        """Test soft delete."""
        pk = rental_item.pk
        rental_item.is_deleted = True
        rental_item.deleted_at = timezone.now()
        rental_item.save()
        assert not RentalItem.objects.filter(pk=pk).exists()
        assert RentalItem.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, rental_item):
        """Test default queryset excludes deleted."""
        rental_item.is_deleted = True
        rental_item.deleted_at = timezone.now()
        rental_item.save()
        assert RentalItem.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, rental_item):
        """Test toggling is_active."""
        original = rental_item.is_active
        rental_item.is_active = not original
        rental_item.save()
        rental_item.refresh_from_db()
        assert rental_item.is_active != original


@pytest.mark.django_db
class TestRental:
    """Rental model tests."""

    def test_create(self, rental):
        """Test Rental creation."""
        assert rental.pk is not None
        assert rental.is_deleted is False

    def test_str(self, rental):
        """Test string representation."""
        assert str(rental) is not None
        assert len(str(rental)) > 0

    def test_soft_delete(self, rental):
        """Test soft delete."""
        pk = rental.pk
        rental.is_deleted = True
        rental.deleted_at = timezone.now()
        rental.save()
        assert not Rental.objects.filter(pk=pk).exists()
        assert Rental.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, rental):
        """Test default queryset excludes deleted."""
        rental.is_deleted = True
        rental.deleted_at = timezone.now()
        rental.save()
        assert Rental.objects.filter(hub_id=hub_id).count() == 0


