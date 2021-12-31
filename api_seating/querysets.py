from django.db import models
from django.db.models.query import QuerySet

class SeatQuerySet(models.QuerySet):
    def are_available(self):
        "returns a queryset with seats that are not blocked"
        booked_ids = [seat.id for seat in self if seat.is_booked() ]
        return self.exclude(id__in=booked_ids, is_blocked=True)

    def not_blocked(self):
        "returns a queryset with seats that are not blocked"
        return self.filter(is_blocked=False)

    def section_rank(self, section, rank):
        return self.filter(row__section=section, rank=rank)

    def rows(self):
        "returns a queryset with all rows in which the seats are located"
        from .models import Row
        return Row.objects.filter(id__in=self.values_list('row'))

class RowQuerySet(models.QuerySet):
    def having_seats_with_rank(self, rank):
        "returns a queryset with rows that has seats for a specific rank"
        from .models import Seat
        row_ids = Seat.objects.with_rank(rank).values_list('row')
        return self.filter(id__in=row_ids)

class OrderQuerySet(models.QuerySet):
    def seats(self):
        "returns a queryset with all seats in orders"
        from .models import Seat
        return Seat.objects.filter(ticket__order__in=self)

    def tickets(self):
        "returns a queryset with all tickets in orders"
        from .models import Ticket
        return Ticket.objects.filter(order__in=self)
