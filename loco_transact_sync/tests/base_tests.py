from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Transaction

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_list_transactions(self):
        # Assume a Transaction model with a user field and a type field
        Transaction.objects.create(user=self.user, type="test_transaction")
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('transactions'))
        self.assertContains(response, "test_transaction")

    def test_signup_view(self):
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  # should redirect

    def test_login_view(self):
        data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)  # should redirect

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # should redirect
