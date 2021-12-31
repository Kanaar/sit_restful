from django.db import models
from api_seating.querysets import SeatQuerySet
from .ticket import Ticket
from django.core.exceptions import ObjectDoesNotExist

class Seat(models.Model):
    objects = SeatQuerySet.as_manager()
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, null=True)
    row = models.ForeignKey("Row", related_name='seats', on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_aisle = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def is_high(self):
        "returns a boolean and checks if the row is located in a balcony section"
        return self.section.is_balcony

    def is_available(self):
        "returns a boolean and checks if the seat is not booked or blocked"
        return not self.is_blocked and not self.is_booked()

    def ticket(self):
        try:
          return Ticket.objects.get(seat=self)
        except ObjectDoesNotExist:
          return None

    def is_booked(self):
        if self.ticket() is None:
          return False
        else:
          return True

