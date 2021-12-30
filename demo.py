import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from api_seating.services import AllocateSeatsService
from api_seating.models import Order

orders = Order.objects.all()
allocation_service = AllocateSeatsService(orders)
allocation_service.call()
allocation_service.print_layout()
