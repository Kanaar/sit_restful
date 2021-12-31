from django.db import models
from .seat import Seat
from api_seating.querysets import OrderQuerySet

class Order(models.Model):
    objects = OrderQuerySet.as_manager()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    section = models.ForeignKey("Section", on_delete=models.CASCADE, null=True)
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, null=True)
    amount_of_tickets = models.IntegerField()
    pref_aisle = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def seats(self):
        return Seat.objects.filter(ticket__order=self)
