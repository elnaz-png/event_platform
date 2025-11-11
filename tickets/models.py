from django.db import models
from django.contrib.auth.models import User
from events.models import Event
from discounts.models import DiscountCode
import uuid
from django.utils import timezone

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    quantity = models.PositiveIntegerField(default=1)

    applied_discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)

    final_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ نهایی (تومان)', default=0)

    registered_at = models.DateTimeField(default=timezone.now, verbose_name='زمان ثبت نام')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    ticket_code = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='کد بلیط')


    def __str__(self):
        return f"{self.event.title} - {self.buyer.username}"
