from api_seating.models import Row, Seat, Ticket

class SimpleSeatingService():
    def __init__(self, orders):
        self.orders = orders
        self.section = orders.first().section
        self.rank = orders.first().rank
        # TODO: check if orders are in same section and rank
        rows, row_ids = self.collect_rows(self.section, self.rank)

        self.rows = rows
        self.row_ids = row_ids

    def call(self):
        "creates tickets for a queryeset of orders"
        for order in self.orders:
            self.allocate_group(order)

    def collect_rows(self, section, rank):
        "returns a tuple (rows, list_of_row_indices) with rows for the specified section and rank"
        seats = Seat.objects.section_rank(section=section, rank=rank)
        row_ids = seats.values_list('row', flat=True).distinct()
        rows = Row.objects.filter(id__in=row_ids)
        return rows, list(row_ids)

    def seats_arranged(self, row):
        """
        returns a queryset with seats to be filled with users for a section
        and rank. The order or seats meanders over the rows
        """
        if self.row_ids.index(row.id) % 2:
            return row.seats.filter(rank=self.rank).order_by('-number')
        else:
            return row.seats.filter(rank=self.rank).order_by('number')

    def allocate_group(self, order):
        "creates tickets for each order and places users in their seats"
        for row in self.rows:
            for seat in self.seats_arranged(row):
                if seat.is_available() == True and order.tickets.count() < order.n_tickets:
                    Ticket.objects.create(order=order, seat=seat)

    def print_layout(self):
        "prints the results"
        row_seats = [row.seats.filter(rank=self.rank).order_by('number') for row in self.rows]
        for seat in row_seats:
            print(seat.values_list('ticket__order__name'))
