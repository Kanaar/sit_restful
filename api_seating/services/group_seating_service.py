from api_seating.models import Row, Seat, Ticket
import numpy as np

class GroupSeatingService():
    def __init__(self, orders, n_attempts):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        self.n_attempts = n_attempts
        # TODO: check if orders are in same section and rank
        self.rows_seats_arranged = self.arrange_row_seats(self.section, self.rank)

    def call(self):
      "creates tickets for a queryeset of orders"
      for order in self.orders:
          self.allocate_to_row(order, self.rows_seats_arranged, self.n_attempts)

    def allocate_to_row(self, order, rows_seats_arranged, n_attempts):
        """
        If the group cant sit together an attempt is
        made on the next n_attempts rows, otherwise the group will be wrapped.
        """
        attempt = 0
        nt = order.amount_of_tickets

        for inx, row_seats in enumerate(rows_seats_arranged):
            if row_seats.are_available().count() > 0 and order.tickets.count() < nt:
                attempt += 1
                group_possible, seat_inx = self.allocate_to_seat(order, row_seats, nt)
                if group_possible == True:
                    self.allocate_tickets(order, rows_seats_arranged, inx, seat_inx)
                elif attempt > n_attempts:
                    self.try_backtrack(order, inx, n_attempts)
                elif inx == len(rows_seats_arranged) - 1:
                    self.try_backtrack(order, inx, n_attempts)
                    # perhaps run this one from the back so not all single chairs are filled
                    # with a large group that nearly fits on the last row

    def try_backtrack(self, order, row_inx, n_attempts):
      if self.backtrack(order, row_inx, n_attempts) == True:
          print('backtracked')
      else:
          print(f'couldnt backtrack order {order}')
          self.allocate_tickets(order, self.rows_seats_arranged, row_inx - n_attempts, 0)

    def backtrack(self, order, row_inx, n_attempts):
      """
      Check if sitting together is possible in the row where prev_order sits if prev_order would
      move one row backward ...Do this max_backtracking iterations ... not when prev_order_seats.count()
      > row_seats.count() / 2
      """
      # to return tuple similar to allocate_to_seat
      if order.amount_of_tickets > (self.rows_seats_arranged[row_inx].not_blocked().count() / 2):
          return False
      else:
          order_inx = list(self.orders).index(order)
          prev_order = self.orders[order_inx-1]
          prev_order2 = self.orders[order_inx-2]
          row_seats = self.rows_seats_arranged[row_inx-1]
          removed_seats = prev_order.seats() | prev_order2.seats()
          availability_bools = [ True if seat in removed_seats else seat.is_available() for seat in row_seats ]

          seat_allocation = self.allocate_to_seat(order, row_seats, order.amount_of_tickets)
          return False

      # rows_seats_arranged[row_inx - 1]
      # Check if sitting together is possible in the row where prev_order sits if prev_order would move one row backward
      # Do this max_backtracking iterations


    def allocate_to_seat(self, order, row_seats, nt):
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

    def allocate_tickets(self, order, rows_seats_arranged, starting_row_index, starting_seat_index):
        # NOTE: could give 'direction' attr to determine the direction of filling the row
        nt = order.amount_of_tickets
        for row_seats in rows_seats_arranged[starting_row_index:]:
            for seat in row_seats:
                if seat.is_available() and nt > 0:
                  nt -= 1
                  Ticket.objects.create(order=order, seat=seat)
                  seat.is_booked = True
                  seat.save()

    def arrange_row_seats(self, section, rank):
        """
        returns a list of querysets with seats for each row given a section and rank
        """
        # NOTE if area size grows this will become too expensive, better build tickets
        # without saving and iterate over row_seats saving after seat placement
        seats = Seat.objects.section_rank(section=section, rank=rank)
        rows_seats_arranged = []

        for inx, row in enumerate(seats.rows()):
            row_seats = seats.filter(row=row)
            if inx % 2:
                rows_seats_arranged.append(row_seats.order_by('-number'))
            else:
                rows_seats_arranged.append(row_seats.order_by('number'))
        return rows_seats_arranged

    def print_layout(self):
        seats_original_order = []
        for inx, row_seats in enumerate(self.rows_seats_arranged):
            if inx % 2:
                seats_original_order.append(row_seats.order_by('number'))
            else:
                seats_original_order.append(row_seats.order_by('number'))

        for row_seats in seats_original_order:
            print(row_seats.values_list('ticket__order__name'))



