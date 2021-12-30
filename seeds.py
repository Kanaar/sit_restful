import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from django.core.management import call_command
from api_seating.models import Rank, Row, Seat, Section

call_command('loaddata', 'fixtures/rank.json')
call_command('loaddata', 'fixtures/section.json')

main = Section.objects.get(name="main")
main_row_lengths = [5, 8, 8, 8, 10, 10]

for row_i, seats in enumerate(main_row_lengths):
  front = True if row_i == 0 else False
  row = Row.objects.create(section=main, number=row_i+1, is_front=front)
  seat_numbers = list(range(1, seats + 1))

  if row_i == 0:
    front = True
    rank = Rank.objects.get(name="1e rang+")
  elif row_i >= 5:
    rank = Rank.objects.get(name="2e rang")
  else:
    rank = Rank.objects.get(name="1e rang")

  for seat_i, seat in enumerate(seat_numbers):
    aisle = True if seat == seat_numbers[0] or seat == seat_numbers[-1] else False
    Seat.objects.create(row=row,
                        number=seat,
                        rank=rank,
                        is_aisle=aisle
                        )

