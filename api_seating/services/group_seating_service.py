from api_seating.models import Row, Seat, Ticket, Order

class GroupSeatingService():
    def __init__(self, orders, n_front, n_back):
          self.orders = orders
          self.n_front = n_front
          self.n_back = n_back
          # TODO: validate if orders are in same section and rank
          section = orders.first().section
          rank = orders.first().rank

          self.section = section
          self.rank = rank

          rows, row_ids = self.collect_rows(self.section, self.rank)

          self.rows = rows
          self.row_ids = row_ids

    def call(self):
      "creates tickets for a queryeset of orders"
      for order in self.orders:
          self.to_row(order, self.n_front, self.n_back)

    def call_verbose(self):
      "creates tickets for a queryeset of orders while printing the layout after every change"
      for order in self.orders:
          self.to_row(order, self.n_front, self.n_back)
          self.print_layout()

    def to_row(self, order, n_front, n_back):
        """
        If the group cant sit together an attempt is
        made on the next n_front rows, otherwise the group will be wrapped.
        """
        attempt = 0
        tried_back = False

        for ri, row in enumerate(self.rows):
            row_seats = self.seats_arranged(row)

            if row_seats.are_available().count() > 0 and order.tickets.count() < order.n_tickets:
                attempt += 1
                grouped, si = self.to_seat(order, row_seats, order.n_tickets)

                if grouped == True:
                    self.to_ticket(order, ri, si)
                elif attempt > n_front:
                    tried_back = self.try_backtrack(order, ri, n_back)
                elif self.last_row(ri) == True:
                    tried_back = self.try_backtrack(order, ri, n_back)
                elif tried_back == True:
                    self.to_ticket(order, ri, 0)
        self.to_ticket(order, 0, 0)

    def to_seat(self, order, row_seats, n_tickets, removed_seats=[]):
        """
        returns a tuple with (bool_grouping_possible, seat_index_to_start).
        Checks if a sequence of n_tickets seats is available next to each other.
        """
        availability_bools = self.availability_bools(row_seats, removed_seats)
        for inx, av_bool in enumerate(availability_bools):
            if self.unchecked_seats(inx, n_tickets, availability_bools) == True:
                if self.placing_possible(inx, n_tickets, availability_bools):
                    return (True, inx)
        return (False, 0)

    def to_ticket(self, order, start_ri, start_si):
        "creates tickets for order"
        for row in self.rows[start_ri:]:
            row_seats = self.seats_arranged(row)[start_si:]
            for seat in row_seats:
                if seat.is_available() == True and order.tickets.count() < order.n_tickets:
                    Ticket.objects.create(order=order, seat=seat)

    def try_backtrack(self, order, ri, n_back):
      "will proceed with backtracking if possible, otherwise returns True to signal an attempt is made"
      group_possible, prev_orders, ri, si = self.backtrack_route(order, ri, n_back)
      if group_possible == True:
          return self.backtrack(order, prev_orders, ri, si)
      else:
          return True

    def backtrack_route(self, order, ri, n_back):
      """
      Returns a tuple (bool_backtrack_possible, order, row_index, seat_index).
      n_back attemts for backtracking will be made
      """
      row_seats = self.seats_arranged(self.rows[ri-1])

      if order.n_tickets > (row_seats.not_blocked().count() / 2):
          return (False, Order.objects.none(), 0, 0)
      else:
          for attempt in list(range(1, n_back + 1)):
              if attempt <= n_back:
                  prev_orders = self.orders.prev_orders(order, attempt)
                  group_possible, si = self.to_seat(order, row_seats, order.n_tickets, prev_orders.seats())
                  if group_possible == True:
                      return (group_possible, prev_orders, ri, si)
          return (False, Order.objects.none(), 0, 0)

    def backtrack(self, order, prev_orders, ri, si):
        """
        Executes backtracking. Previous order placements are removed and tickets are created for
        order after which the previous orders restart their ticket allocation
        """
        adj_ri = self.adjusted_row_index(prev_orders)
        prev_orders.tickets().delete()
        self.to_ticket(order, adj_ri, si)
        for prev_order in prev_orders:
            self.to_row(prev_order, self.n_front, self.n_back)

    def availability_bools(self, row_seats, removed_seats=[]):
        "Returns a list of booleans indexed as the row seats. True for available seat"
        availability_bools = []
        for seat in row_seats:
          if seat in removed_seats:
            availability_bools.append(True)
          else:
            availability_bools.append(seat.is_available())
        return availability_bools

    def last_row(self, ri):
        "returns True if row index ri is at the last row in self.rows"
        return ri == len(self.row_ids) - 1

    def unchecked_seats(self, inx, n_tickets, availability_bools):
        """
        returns a boolean. Checks if the there are still seats left in availability_bools
        to attempt placing
        """
        return (inx + n_tickets) <= len(availability_bools)

    def placing_possible(self, inx, n_tickets, availability_bools):
        """
        returns a boolean. Checks if consecutive n_tickets can be placed (i.e. no
        unavailable seat is in between
        """
        return False not in availability_bools[inx:inx+n_tickets]

    def adjusted_row_index(self, prev_orders):
        "returns an integer. Returns the row index of the first of the previous order seats"
        starting_seat = prev_orders.seats().first()
        adjusted_row_index = self.row_ids.index(starting_seat.row.id)
        return adjusted_row_index

    def collect_rows(self, section, rank):
        "returns a tuple (rows, list_of_row_indices) with rows for the specified section and rank"
        seats = Seat.objects.section_rank(section=section, rank=rank)
        row_ids = seats.values_list('row', flat=True).distinct()
        rows = Row.objects.filter(id__in=row_ids)
        return rows, list(row_ids)

    def seats_arranged(self, row):
        """
        returns a queryset with seats to be filled with users for a section and rank.
        The order or seats meanders over the rows
        """

        if self.row_ids.index(row.id) % 2:
            return row.seats.filter(rank=self.rank).order_by('-number')
        else:
            return row.seats.filter(rank=self.rank).order_by('number')

    def print_layout(self):
        "prints the layout"
        row_seats = [row.seats.filter(rank=self.rank).order_by('number') for row in self.rows]
        print("_____________")
        for seat in row_seats:
            print(seat.values_list('ticket__order__name'))
        print("_____________")

