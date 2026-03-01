"""AI tools for the Rentals module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListRentalItems(AssistantTool):
    name = "list_rental_items"
    description = "List items available for rent."
    module_id = "rentals"
    required_permission = "rentals.view_rentalitem"
    parameters = {
        "type": "object",
        "properties": {"is_available": {"type": "boolean"}, "category": {"type": "string"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from rentals.models import RentalItem
        qs = RentalItem.objects.filter(is_active=True)
        if 'is_available' in args:
            qs = qs.filter(is_available=args['is_available'])
        if args.get('category'):
            qs = qs.filter(category__icontains=args['category'])
        return {"items": [{"id": str(i.id), "name": i.name, "code": i.code, "daily_rate": str(i.daily_rate), "is_available": i.is_available, "category": i.category, "quantity_total": i.quantity_total} for i in qs]}


@register_tool
class CreateRentalItem(AssistantTool):
    name = "create_rental_item"
    description = "Create a rental item."
    module_id = "rentals"
    required_permission = "rentals.add_rentalitem"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}, "code": {"type": "string"}, "description": {"type": "string"},
            "daily_rate": {"type": "string"}, "category": {"type": "string"},
            "quantity_total": {"type": "integer"},
        },
        "required": ["name", "daily_rate"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from rentals.models import RentalItem
        i = RentalItem.objects.create(name=args['name'], code=args.get('code', ''), description=args.get('description', ''), daily_rate=Decimal(args['daily_rate']), category=args.get('category', ''), quantity_total=args.get('quantity_total', 1))
        return {"id": str(i.id), "name": i.name, "created": True}


@register_tool
class ListRentals(AssistantTool):
    name = "list_rentals"
    description = "List rental agreements."
    module_id = "rentals"
    required_permission = "rentals.view_rental"
    parameters = {
        "type": "object",
        "properties": {"status": {"type": "string", "description": "reserved, active, returned, overdue, cancelled"}, "limit": {"type": "integer"}},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from rentals.models import Rental
        qs = Rental.objects.select_related('item', 'customer').all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {"rentals": [{"id": str(r.id), "reference": r.reference, "item": r.item.name if r.item else None, "customer_name": r.customer_name, "status": r.status, "start_date": str(r.start_date), "end_date": str(r.end_date), "total": str(r.total)} for r in qs.order_by('-start_date')[:limit]]}


@register_tool
class CreateRental(AssistantTool):
    name = "create_rental"
    description = "Create a rental agreement."
    module_id = "rentals"
    required_permission = "rentals.add_rental"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "item_id": {"type": "string"}, "customer_name": {"type": "string"},
            "start_date": {"type": "string"}, "end_date": {"type": "string"},
            "deposit_amount": {"type": "string"}, "notes": {"type": "string"},
        },
        "required": ["item_id", "customer_name", "start_date", "end_date"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from rentals.models import Rental
        r = Rental.objects.create(
            item_id=args['item_id'], customer_name=args['customer_name'],
            start_date=args['start_date'], end_date=args['end_date'],
            deposit_amount=Decimal(args['deposit_amount']) if args.get('deposit_amount') else None,
            notes=args.get('notes', ''),
        )
        return {"id": str(r.id), "reference": r.reference, "created": True}
