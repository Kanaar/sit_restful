from api_seating.models import Row, Seat, Ticket
import numpy as np

class SimpleSeatingService():
    def __init__(self, orders):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        # TODO: check if orders are in same section and rank
        self.seats_ordered = self.ordered_section_seats(self.section, self.rank)

    def call(self):
      "creates tickets for a queryeset of orders"
      for order in self.orders:
          self.allocate_group(order, self.seats_ordered)

    def ordered_section_seats(self, section, rank):
        """
        returns a queryset with seats to be filled with users for a section
        and rank. The order or seats meanders over the rows
        """
        # NOTE if area size grows this will become too expensive
        seats = Seat.objects.section_rank(section=section, rank=rank)
        seats_ordered = np.array([])

        for inx, row in enumerate(seats.rows()):
            row_seats = seats.filter(row=row)
            if inx % 2:
                array = np.array(row_seats.order_by('-number'))
            else:
                array = np.array(row_seats.order_by('number'))
            seats_ordered = np.append(seats_ordered, array)
        return seats_ordered

    def allocate_group(self, order, seats_ordered):
        "creates tickets for each order and places users in their seats"
        nt = order.amount_of_tickets
        for seat in seats_ordered[:nt]:
            Ticket.objects.create(order=order, seat=seat)
        self.seats_ordered = np.delete(seats_ordered, list(range(nt)))

    def print_layout(self):
        row_ids = Seat.objects.filter(rank=self.rank).values_list('row')
        rows = Row.objects.filter(id__in=row_ids, section=self.section)
        row_seats = [Seat.objects.filter(row=row, rank=self.rank).order_by('number') for row in rows]

        for seat in row_seats:
            print(seat.values_list('ticket__order__name'))
