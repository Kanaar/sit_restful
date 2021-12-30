from django.db import models

class Row(models.Model):
    section = models.ForeignKey("Section", on_delete=models.CASCADE, null=True)
    number = models.IntegerField()
    is_front = models.BooleanField(default=False)

