"""
AI context for the Rentals module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Rentals

### Models

**RentalItem**
- `name` (str, required), `code` (str, optional), `description` (text)
- `daily_rate` (decimal — price per day), `category` (str, optional), `location` (str, optional)
- `quantity_total` (int, default 1 — total units available for this item)
- `is_available` (bool, default True), `is_active` (bool, default True)

**Rental**
- `reference` (str, required), `item` (FK → RentalItem, CASCADE)
- `customer_name` (str, required), `customer` (FK → customers.Customer, SET_NULL, nullable)
- `status` choices: reserved | active | returned | overdue | cancelled (default: reserved)
- `start_date`, `end_date` (dates, required)
- `total` (decimal — calculated: days × daily_rate)
- `deposit_amount` (decimal), `deposit_paid` (bool), `deposit_returned` (bool)
- `condition_out` (text — item condition at checkout), `condition_in` (text — item condition at return)
- `notes`

**RentalBlackout**
- `item` (FK → RentalItem, CASCADE, related_name='blackouts')
- `start_date`, `end_date` (dates), `reason` (str)
- Marks periods when an item is unavailable (maintenance, reserved, etc.).

### Key Flows

1. **Add item**: create RentalItem with name, daily_rate, and quantity_total.
2. **Create reservation**: create Rental with status='reserved', set start_date/end_date, fill customer info.
3. **Checkout**: update status to 'active', record condition_out, mark deposit_paid if collected.
4. **Return**: update status to 'returned', record condition_in, set deposit_returned if refunded.
5. **Overdue**: update status to 'overdue' if end_date has passed and item not returned.
6. **Block availability**: create RentalBlackout to prevent bookings during a period.

### Relationships

- Rental → RentalItem (CASCADE), Rental → customers.Customer (SET_NULL).
- RentalBlackout → RentalItem (CASCADE).
- No automatic availability calculation — manage is_available on RentalItem manually.
"""
