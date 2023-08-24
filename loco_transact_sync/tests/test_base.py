# tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Transaction
from ..forms import SignupForm, LoginForm

class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user1', 'user1@example.com', 'password')
        
        # Creating transactions for testing
        Transaction.objects.create(user=self.user, type="credit", amount=1000)
        Transaction.objects.create(user=self.user, type="debit", amount=500)
        
        self.signup_url = reverse('signup_view')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout_view')
        self.transactions_url = reverse('transactions')

    def test_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
        data = {'username': 'testuser', 'password': 'somepassword'}
        response = self.client.post(self.signup_url, data)
        self.assertEquals(response.status_code, 302)  # Redirect after POST

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        data = {'username': 'user1', 'password': 'password'}
        response = self.client.post(self.login_url, data)
        self.assertEquals(response.status_code, 302)  # Redirect after POST

    def test_logout_view(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(self.logout_url)
        self.assertEquals(response.status_code, 302)  # Redirect after logout

    def test_list_transactions(self):
        self.client.login(username='user1', password='password')
        response = self.client.get(self.transactions_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_list.html')
        self.assertTrue('transactions' in response.context)

        # testing search
        response = self.client.get(self.transactions_url, {'search': 'credit'})
        self.assertEquals(response.status_code, 200)
        self.assertTrue('transactions' in response.context)

    def test_authentication_required(self):
        # When not logged in
        response = self.client.get(self.transactions_url)
        self.assertEquals(response.status_code, 302)  # Redirected to login