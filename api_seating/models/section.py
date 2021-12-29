from django.db import models
POSITION_CHOICES = [
  ('l', 'left'),
  ('c', 'centre'),
  ('r', 'right'),
  ('ll', 'outer left'),
  ('rr', 'outer right')
]

class Section(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='c')
    is_balcony = models.BooleanField(default=False)
    is_loge = models.BooleanField(default=False)

    def capacity(self):
        "max number of seats"
        pass
