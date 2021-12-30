from .models import Row, Seat, Ticket
import numpy as np

class AllocateSeatsService():
    def __init__(self, orders):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        # TODO: check if orders are in same section and rank
        self.seats_ordered = self.ordered_section_seats(self.section, self.rank)

    def call(self):
      "creates tickets for a queryeset of orders"
      import ipdb;ipdb.set_trace()
      for order in self.orders:
          pass

    def ordered_section_seats(self, section, rank):
        """
        returns a queryset with seats to be filled with users for a section
        and rank. The order or seats meanders over the rows
        """
        row_ids = Seat.objects.filter(rank=self.rank).values_list('row')
        rows = Row.objects.filter(id__in=row_ids, section=self.section)
        seats = Seat.objects.filter(row__in=rows, rank=rank)
        seats_ordered = np.array([])

        for inx, row in enumerate(rows):
            row_seats = seats.filter(row=row)
            if inx % 2:
                array = np.array(row_seats.order_by('-number'))
            else:
                array = np.array(row_seats.order_by('number'))
            seats_ordered = np.append(seats_ordered, array)
        return seats_ordered




