from django.db import models

class Row(models.Model):
    section = models.ForeignKey("Section", on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_front = models.BooleanField(default=False)

    def is_high(self):
        "returns a boolean and checks if the row is located in a balcony section"
        return self.section.is_balcony

    def is_available(self):
        "returns a boolean and checks if the seat is not booked or blocked"
        return not self.is_blocked and not self.is_booked

