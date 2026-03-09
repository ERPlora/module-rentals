# Rental Management

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `rentals` |
| **Version** | `1.0.0` |
| **Icon** | `key-outline` |
| **Dependencies** | None |

## Models

### `RentalItem`

RentalItem(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, code, description, daily_rate, is_available, is_active, category, location, quantity_total)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `code` | CharField | max_length=50, optional |
| `description` | TextField | optional |
| `daily_rate` | DecimalField |  |
| `is_available` | BooleanField |  |
| `is_active` | BooleanField |  |
| `category` | CharField | max_length=100, optional |
| `location` | CharField | max_length=255, optional |
| `quantity_total` | PositiveIntegerField |  |

### `Rental`

Rental(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, reference, item, customer_name, status, start_date, end_date, total, customer, deposit_amount, deposit_paid, deposit_returned, condition_out, condition_in, notes)

| Field | Type | Details |
|-------|------|---------|
| `reference` | CharField | max_length=50 |
| `item` | ForeignKey | → `rentals.RentalItem`, on_delete=CASCADE |
| `customer_name` | CharField | max_length=255 |
| `status` | CharField | max_length=20, choices: reserved, active, returned, overdue, cancelled |
| `start_date` | DateField |  |
| `end_date` | DateField |  |
| `total` | DecimalField |  |
| `customer` | ForeignKey | → `customers.Customer`, on_delete=SET_NULL, optional |
| `deposit_amount` | DecimalField |  |
| `deposit_paid` | BooleanField |  |
| `deposit_returned` | BooleanField |  |
| `condition_out` | TextField | optional |
| `condition_in` | TextField | optional |
| `notes` | TextField | optional |

### `RentalBlackout`

Dates when a rental item is unavailable (maintenance, reserved, etc.).

| Field | Type | Details |
|-------|------|---------|
| `item` | ForeignKey | → `rentals.RentalItem`, on_delete=CASCADE |
| `start_date` | DateField |  |
| `end_date` | DateField |  |
| `reason` | CharField | max_length=255, optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Rental` | `item` | `rentals.RentalItem` | CASCADE | No |
| `Rental` | `customer` | `customers.Customer` | SET_NULL | Yes |
| `RentalBlackout` | `item` | `rentals.RentalItem` | CASCADE | No |

## URL Endpoints

Base path: `/m/rentals/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `items/` | `items` | GET |
| `rental_items/` | `rental_items_list` | GET |
| `rental_items/add/` | `rental_item_add` | GET/POST |
| `rental_items/<uuid:pk>/edit/` | `rental_item_edit` | GET |
| `rental_items/<uuid:pk>/delete/` | `rental_item_delete` | GET/POST |
| `rental_items/<uuid:pk>/toggle/` | `rental_item_toggle_status` | GET |
| `rental_items/bulk/` | `rental_items_bulk_action` | GET/POST |
| `items/<uuid:pk>/` | `rental_item_detail` | GET |
| `items/<uuid:pk>/blackouts/add/` | `blackout_add` | GET/POST |
| `items/<uuid:pk>/blackouts/panel/` | `blackout_add_panel` | GET/POST |
| `items/<uuid:pk>/blackouts/<uuid:blackout_pk>/delete/` | `blackout_delete` | GET/POST |
| `rentals/` | `rentals_list` | GET |
| `rentals/add/` | `rental_add` | GET/POST |
| `rentals/<uuid:pk>/edit/` | `rental_edit` | GET |
| `rentals/<uuid:pk>/delete/` | `rental_delete` | GET/POST |
| `rentals/bulk/` | `rentals_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `rentals.view_rental` | View Rental |
| `rentals.add_rental` | Add Rental |
| `rentals.change_rental` | Change Rental |
| `rentals.delete_rental` | Delete Rental |
| `rentals.view_rentalitem` | View Rentalitem |
| `rentals.add_rentalitem` | Add Rentalitem |
| `rentals.change_rentalitem` | Change Rentalitem |
| `rentals.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_rental`, `add_rentalitem`, `change_rental`, `change_rentalitem`, `view_rental`, `view_rentalitem`
- **employee**: `add_rental`, `view_rental`, `view_rentalitem`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Items | `cube-outline` | `items` | No |
| Rentals | `key-outline` | `rentals` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_rental_items`

List items available for rent.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `is_available` | boolean | No |  |
| `category` | string | No |  |

### `create_rental_item`

Create a rental item.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes |  |
| `code` | string | No |  |
| `description` | string | No |  |
| `daily_rate` | string | Yes |  |
| `category` | string | No |  |
| `quantity_total` | integer | No |  |

### `list_rentals`

List rental agreements.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | reserved, active, returned, overdue, cancelled |
| `limit` | integer | No |  |

### `create_rental`

Create a rental agreement.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `item_id` | string | Yes |  |
| `customer_name` | string | Yes |  |
| `start_date` | string | Yes |  |
| `end_date` | string | Yes |  |
| `deposit_amount` | string | No |  |
| `notes` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  rentals/
    css/
    js/
templates/
  rentals/
    pages/
      blackout_add.html
      dashboard.html
      index.html
      items.html
      rental_add.html
      rental_edit.html
      rental_item_add.html
      rental_item_detail.html
      rental_item_edit.html
      rental_items.html
      rentals.html
      settings.html
    partials/
      blackout_add_content.html
      blackouts_list.html
      dashboard_content.html
      items_content.html
      panel_blackout_add.html
      panel_rental_add.html
      panel_rental_edit.html
      panel_rental_item_add.html
      panel_rental_item_edit.html
      rental_add_content.html
      rental_edit_content.html
      rental_item_add_content.html
      rental_item_detail_content.html
      rental_item_edit_content.html
      rental_items_content.html
      rental_items_list.html
      rentals_content.html
      rentals_list.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
