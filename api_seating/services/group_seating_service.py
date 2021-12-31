from api_seating.models import Row, Seat, Ticket, Order
import numpy as np

class GroupSeatingService():
    def __init__(self, orders, n_forward, n_backward):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        self.n_forward = n_forward
        self.n_backward = n_backward
        # TODO: check if orders are in same section and rank
        self.rows_seats_arranged = self.arrange_row_seats(self.section, self.rank)
        # TODO change nt to ntickets

    def call(self):
      "creates tickets for a queryeset of orders"
      for order in self.orders:
          self.allocate_to_row(order, self.rows_seats_arranged, self.n_forward, self.n_backward)

    def allocate_to_row(self, order, rows_seats_arranged, n_forward, n_backward):
        """
        If the group cant sit together an attempt is
        made on the next n_forward rows, otherwise the group will be wrapped.
        """
        attempt = 0
        nt = order.amount_of_tickets
        backtracked = False
        print(order)
        for inx, row_seats in enumerate(rows_seats_arranged):
            if row_seats.are_available().count() > 0 and order.tickets.count() < nt:
                attempt += 1
                group_possible, seat_inx = self.allocate_to_seat(order, row_seats, nt)
                if group_possible == True:
                    self.allocate_tickets(order, rows_seats_arranged, inx, seat_inx)
                elif attempt > n_forward:
                    backtracked = self.try_backtrack(order, inx, n_backward)
                elif inx == len(rows_seats_arranged) - 1:
                    backtracked = self.try_backtrack(order, inx, n_backward)
                elif backtracked == True:
                    self.allocate_tickets(order, rows_seats_arranged, inx, 0)
                    # perhaps run this one from the back so not all single chairs are filled
                    # with a large group that nearly fits on the last row

    def try_backtrack(self, order, row_inx, n_backward):
      group_possible, prev_orders, row_inx, seat_inx = self.backtrack_route(order, row_inx, n_backward)

      if group_possible == True:
          return self.backtrack(order, prev_orders, row_inx, seat_inx)
      else:
          return True


    def backtrack_route(self, order, row_inx, n_backward):
      """
      Check if sitting together is possible in the row where prev_order sits if prev_order would
      move one row backward ...Do this max_backtracking iterations ... not when prev_order_seats.count()
      > row_seats.count() / 2
      """
      # to return tuple similar to allocate_to_seat
      row_seats = self.rows_seats_arranged[row_inx-1]
      if order.amount_of_tickets > (row_seats.not_blocked().count() / 2):
          return (False, Order.objects.none(), 0, 0)
      else:
          for attempt in list(range(1, n_backward + 1)):
              nt = order.amount_of_tickets
              order_inx = list(self.orders).index(order)
              if attempt <= n_backward:
                  prev_orders_ids = [order.id for order in self.orders[order_inx-attempt : order_inx]]
                  prev_orders = self.orders.filter(id__in=prev_orders_ids)
                  group_possible, seat_inx = self.allocate_to_seat(order, row_seats, nt, prev_orders.seats())
                  if group_possible == True:
                      return (group_possible, prev_orders, row_inx, seat_inx)
          return (False, Order.objects.none(), 0, 0)

    def backtrack(self, order, prev_orders, row_inx, seat_inx):
        "execute backtracking"
        first_seat = prev_orders.seats().first()

        for row_seats in self.rows_seats_arranged:
            if first_seat in row_seats:
                adj_row_inx = self.rows_seats_arranged.index(row_seats)

        prev_orders.tickets().delete()
        self.allocate_tickets(order, self.rows_seats_arranged, adj_row_inx, seat_inx)

        for prev_order in prev_orders:
            # self.allocate_tickets(prev_order, self.rows_seats_arranged, adj_row_inx, seat_inx)
            self.allocate_to_row(prev_order, self.rows_seats_arranged, self.n_forward, self.n_backward)
        # instead of creating and deleting tickets. Compile a dict and create all tickets at the end of
        # the algorithm execution

    def availability_bools(self, row_seats, removed_seats=[]):
        availability_bools = []
        for seat in row_seats:
          if seat in removed_seats:
            availability_bools.append(True)
          else:
            availability_bools.append(seat.is_available())
        return availability_bools

    def allocate_to_seat(self, order, row_seats, nt, removed_seats=[]):
        """
        returns a tuple with (bool_grouping_possible, seat_index_to_start). Checks if a sequence of nt seats is available next to each other.
        """
        availability_bools = self.availability_bools(row_seats, removed_seats)
        for inx, av_bool in enumerate(availability_bools):
            if (inx + nt) <= len(availability_bools):
                if self.placing_possible(inx, nt, availability_bools):
                    return (True, inx)
        return (False, 0)

    def placing_possible(self, inx, nt, availability_bools):
        return False not in availability_bools[inx:inx+nt]

    def allocate_tickets(self, order, rows_seats_arranged, starting_row_index, starting_seat_index):
        # NOTE: could give 'direction' attr to determine the direction of filling the row
        nt = order.amount_of_tickets
        for row_seats in rows_seats_arranged[starting_row_index:]:
            for seat in row_seats:
                if seat.is_available() and nt > 0:
                  nt -= 1
                  Ticket.objects.create(order=order, seat=seat)

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



