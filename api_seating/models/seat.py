from django.db import models

class Seat(models.Model):
    rank = models.ForeignKey("Rank", on_delete=models.CASCADE, null=True)
    row = models.ForeignKey("Row", on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_aisle = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_booked = models.BooleanField(default=False)

    def is_high(self):
        "returns a boolean and checks if the row is located in a balcony section"
        return self.section.is_balcony

    def is_available(self):
        "returns a boolean and checks if the seat is not booked or blocked"
        return not self.is_blocked and not self.is_booked

