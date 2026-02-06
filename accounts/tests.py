# accounts/tests.py
from django.test import TestCase
from django.urls import reverse

class AccountsPageTest(TestCase):
    def test_login_page_status_code(self):
        """چک می‌کند صفحه لاگین با موفقیت (کد 200) باز شود"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_status_code(self):
        """چک می‌کند صفحه ثبت‌نام با موفقیت باز شود"""
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)