from django.db import models

class Seat(models.Model):
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, null=True)
    row = models.ForeignKey("Row", on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_aisle = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)

