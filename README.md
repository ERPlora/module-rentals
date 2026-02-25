# Rental Management Module

Equipment, vehicle and space rental management.

## Features

- Maintain a catalog of rental items with daily rates, categories, locations, and quantity tracking
- Create and manage rentals with full lifecycle tracking (reserved, active, returned, overdue, cancelled)
- Track rental periods with start and end dates
- Manage deposits (amount, payment status, return status)
- Record item condition at checkout and return
- Define blackout periods for items (maintenance, reserved blocks, etc.)
- Link rentals to customer records
- Toggle item availability and active status

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Rental Management > Settings**

## Usage

Access via: **Menu > Rental Management**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/rentals/dashboard/` | Overview of rental activity |
| Items | `/m/rentals/items/` | Manage rental item catalog |
| Rentals | `/m/rentals/rentals/` | List and manage rental agreements |
| Settings | `/m/rentals/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `RentalItem` | Rentable item with name, code, description, daily rate, category, location, quantity, and availability flags |
| `Rental` | Rental agreement with reference, linked item and customer, dates, status, total, deposit tracking, and condition notes |
| `RentalBlackout` | Unavailability period for a rental item with date range and reason |

## Permissions

| Permission | Description |
|------------|-------------|
| `rentals.view_rental` | View rentals |
| `rentals.add_rental` | Create new rentals |
| `rentals.change_rental` | Edit existing rentals |
| `rentals.delete_rental` | Delete rentals |
| `rentals.view_rentalitem` | View rental items |
| `rentals.add_rentalitem` | Create new rental items |
| `rentals.change_rentalitem` | Edit existing rental items |
| `rentals.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
