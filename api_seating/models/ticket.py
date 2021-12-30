from django.db import models

class Ticket(models.Model):
    order = models.ForeignKey("Order", related_name='tickets', on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, null=True)
