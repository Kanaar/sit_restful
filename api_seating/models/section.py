from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=50)
    is_balcony = models.BooleanField(default=False)
    is_loge = models.BooleanField(default=False)

    def capacity(self):
        "max number of seats"
        pass
