
from django.db import models
from events.models import Event 

class DiscountCode(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='discount_codes')
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    percent = models.PositiveIntegerField(verbose_name='درصد تخفیف')
    
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='محدودیت استفاده')

    def __str__(self):
         return f"{self.code} - {self.percent}%"