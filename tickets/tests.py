# tickets/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from events.models import Event
from .models import Ticket

class TicketModelTest(TestCase):
    def setUp(self):
        # ساخت کاربر و رویداد پیش‌نیاز
        self.user = User.objects.create_user(username='buyer', password='password123')
        self.organizer = User.objects.create_user(username='org', password='password123')
        self.event = Event.objects.create(
            organizer=self.organizer, title='Concert', price=1000, capacity=50
        )

    def test_ticket_creation(self):
        """تست ساخت بلیط در دیتابیس"""
        ticket = Ticket.objects.create(
            event=self.event,
            buyer=self.user,
            quantity=2,
            final_price=2000
        )
        # چک می‌کنیم که بلیط ساخته شده و کد پیگیری دارد
        self.assertEqual(ticket.buyer.username, 'buyer')
        self.assertEqual(ticket.quantity, 2)
        self.assertTrue(ticket.ticket_code) # چک می‌کند کد بلیط خالی نباشد