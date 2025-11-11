from django.db import models
from django.contrib.auth.models import User
from tickets.models import Ticket

class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        SUCCESS = 'SUCCESS', 'موفق'
        FAILED = 'FAILED', 'ناموفق'
        PENDING = 'PENDING', 'در انتظار'

    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='خریدار')
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, verbose_name='بلیط مرتبط')
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ (تومان)')
    status = models.CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING, verbose_name='وضعیت')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    

    updated_at = models.DateTimeField(auto_now=True, verbose_name='زمان به‌روزرسانی')
    
    
    tracking_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد رهگیری')

    def __str__(self):
        return f"تراکنش {self.id} - {self.get_status_display()}"