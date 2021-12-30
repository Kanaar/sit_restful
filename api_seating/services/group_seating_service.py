from api_seating.models import Row, Seat, Ticket
import numpy as np

class GroupSeatingService():
    def __init__(self, orders, n_attempts):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        self.n_attempts = n_attempts
        # TODO: check if orders are in same section and rank
        self.seats_ordered = self.ordered_section_seats(self.section, self.rank)

    def call(self):
      # NOTE realized that a backtracking algorithm could be suitable
      # NOTE change name seats_ordered to seats_sequenced
      "creates tickets for a queryeset of orders"
      for order in self.orders:
          self.try_grouping(order, self.seats_ordered, self.n_attempts)

    def try_grouping(self, order, seats_ordered, n_attempts):
        # NOTE: this is actually finding appropriate row index
        """
        If the group cant sit together an attempt is
        made on the next n_attempts rows, otherwise the group will be wrapped.
        """
        attempt = 0
        nt = order.amount_of_tickets

        for inx, row_seats in enumerate(seats_ordered):
            available_seats = row_seats.filter(is_blocked=False, is_booked=False)
            if available_seats.count() > 0 and order.tickets.count() < nt:
                attempt += 1
                group_possible, seat_inx = self.grouping_possible_at(order, row_seats, nt)
                if group_possible == True:
                    self.allocate_group(order, seats_ordered, inx, seat_inx)
                elif attempt > n_attempts:
                    self.allocate_group(order, seats_ordered, inx - n_attempts, 0)

    def ordered_section_seats(self, section, rank):
        """
        returns a list of querysets with seats for each row given a section and rank
        """
        # NOTE if area size grows this will become too expensive, better build tickets
        # without saving and iterate over row_seats saving after seat placement
        row_ids = Seat.objects.filter(rank=rank).values_list('row')
        rows = Row.objects.filter(id__in=row_ids, section=section)
        seats = Seat.objects.filter(row__in=rows, rank=rank)
        seats_ordered = []

        for inx, row in enumerate(rows):
            row_seats = seats.filter(row=row)
            if inx % 2:
                seats_ordered.append(row_seats.order_by('-number'))
            else:
                seats_ordered.append(row_seats.order_by('number'))
        return seats_ordered

    def grouping_possible_at(self, order, row_seats, nt):
        # NOTE: this is actually finding appropriate seat index
        """
        returns a tuple with (bool_grouping_possible, seat_index_to_start). Checks if a sequence of nt seats is available next to each other.
        """
        availability_bools = [ seat.is_available() for seat in row_seats ]
        for inx, av_bool in enumerate(availability_bools):
            if (inx + nt) <= len(availability_bools):
                placing_attempt = [availability_bools[i] for i in list(range(inx, inx + nt))]
                if False not in placing_attempt:
                    return (True, inx)
            else:
                return (False, 0)

    def allocate_group(self, order, seats_ordered, starting_row_index, starting_seat_index):
        nt = order.amount_of_tickets
        for row_seats in seats_ordered[starting_row_index:]:
            for seat in row_seats:
                if seat.is_available() and nt > 0:
                  nt -= 1
                  Ticket.objects.create(order=order, seat=seat)
                  seat.is_booked = True
                  seat.save()

    def print_layout(self):
        seats_original_order = []
        for inx, row_seats in enumerate(self.seats_ordered):
            if inx % 2:
                seats_original_order.append(row_seats.order_by('number'))
            else:
                seats_original_order.append(row_seats.order_by('number'))

        for row_seats in seats_original_order:
            print(row_seats.values_list('ticket__order__name'))



