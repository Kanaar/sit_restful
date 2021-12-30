import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from api_seating.services import SimpleSeatingService
from api_seating.models import Order

orders = Order.objects.all()
simple_service = SimpleSeatingService(orders)
simple_service.call()
simple_service.print_layout()
