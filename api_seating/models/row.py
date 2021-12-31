from django.db import models
from api_seating.querysets import RowQuerySet

class Row(models.Model):
    objects = RowQuerySet.as_manager()
    section = models.ForeignKey("Section", on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_front = models.BooleanField(default=False)

