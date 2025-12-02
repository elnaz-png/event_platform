
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class UserType(models.TextChoices):
        ORGANIZER = 'ORGANIZER', 
        ATTENDER = 'ATTENDER', 

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=UserType.choices, verbose_name= 'user type')

    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='phone number')

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
