from django.db import models
from events.models import Event   

class DiscountCode(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    percent = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} - {self.percent}%"
