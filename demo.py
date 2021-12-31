import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from api_seating.services import SimpleSeatingService, GroupSeatingService
from api_seating.models import Order
import timeit

orders = Order.objects.all()
start = timeit.default_timer()

# -----------------------------------------
# --------Toggle algorithms below----------
# -----------------------------------------
simple_service = SimpleSeatingService(orders)
simple_service.call()
simple_service.print_layout()

# improved_service = GroupSeatingService(orders, 1, 2)
# improved_service.call()
# # improved_service.call_verbose()
# improved_service.print_layout()

# -----------------------------------------

stop = timeit.default_timer()
print('Time: ', stop - start)
