from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    class EventStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'پیش‌نویس'
        PUBLISHED = 'PUBLISHED', 'منتشر شده'
        CANCELLED = 'CANCELLED', 'لغو شده'

    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events'
    )

    title = models.CharField(max_length=200, verbose_name='عنوان')
    location = models.CharField(max_length=300, verbose_name='مکان')
    event_time = models.DateTimeField(default=timezone.now)

    price = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='مبلغ (تومان)', default=0
    )

    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت', null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=EventStatus.choices,
        default=EventStatus.DRAFT, verbose_name='وضعیت'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
