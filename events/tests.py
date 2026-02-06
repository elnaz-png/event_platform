from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event

class EventModelTest(TestCase):
    def setUp(self):
        # این تابع قبل از هر تست اجرا می‌شود و داده‌های الکی (Mock) می‌سازد
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.event = Event.objects.create(
            organizer=self.user,
            title='Test Event',
            description='This is a test description',
            price=50000,
            capacity=100,
            status=Event.EventStatus.PUBLISHED
        )

    def test_event_creation(self):
        """تست می‌کند که آیا رویداد با موفقیت در دیتابیس ساخته شده؟"""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.organizer.username, 'testuser')

    def test_event_list_view(self):
        """تست می‌کند که آیا صفحه لیست رویدادها (URL) بدون خطا بالا می‌آید؟"""
        # آدرس events:list را صدا می‌زند
        response = self.client.get(reverse('events:list'))
        
        # چک می‌کند کد وضعیت 200 (یعنی سالم) باشد
        self.assertEqual(response.status_code, 200) 
        
        # چک می‌کند که اسم رویداد ما در صفحه دیده می‌شود
        self.assertContains(response, 'Test Event')