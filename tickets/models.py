from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    used_discount = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event.title} - {self.buyer.username}"
