import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from api_seating.services import AllocateSeatsService

allocation_service = AllocateSeatsService()
print(allocation_service.call())
