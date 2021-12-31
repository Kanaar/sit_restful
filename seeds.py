import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit_restful.settings")
import django; django.setup()
from django.core.management import call_command
from api_seating.models import Rank, Row, Seat, Section, Order

call_command('loaddata', 'fixtures/rank.json')
call_command('loaddata', 'fixtures/section.json')

main = Section.objects.get(name="main")
main_row_lengths = [5, 8, 8, 8, 10, 10]

# -- Creating rows --
print('creating rows')
for row_i, seats in enumerate(main_row_lengths):
  front = True if row_i == 0 else False
  row = Row.objects.create(section=main, number=row_i+1, is_front=front)
  seat_numbers = list(range(1, seats + 1))

  if row_i == 0:
    front = True
    rank = Rank.objects.get(name="1e rang+")
  elif row_i >= 4:
    rank = Rank.objects.get(name="2e rang")
  else:
    rank = Rank.objects.get(name="1e rang")

  # -- Creating seats --
  print(f'creating seats for row {row.number}')
  for seat_i, seat in enumerate(seat_numbers):
    aisle = True if seat == seat_numbers[0] or seat == seat_numbers[-1] else False
    Seat.objects.create(row=row,
                        number=seat,
                        rank=rank,
                        is_aisle=aisle
                        )

# -- Creating orders --
print('creating orders')
groups_of_users = [1, 3, 4, 4, 5, 1, 2, 4]
names_of_groups = ["A", "B", "C", "D", "E", "F", "G", "H"]

for i, group in enumerate(groups_of_users):
    Order.objects.create(
      name=names_of_groups[i],
      email=f"{names_of_groups[1]}@email.com",
      rank= Rank.objects.get(name="1e rang"),
      n_tickets=group,
      pref_aisle=False,
      section=main
      )
