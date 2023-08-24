# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Transaction
from django.urls import reverse

class DependentsAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user1', 'user1@example.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.transaction = Transaction.objects.create(user=self.user, amount=1000, type='credit')

    def test_get_transaction_by_type(self):
        url = reverse('get_transaction_by_type', kwargs={'type': 'credit'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.transaction.id, response.json())

    def test_get_transaction_sum(self):
        url = reverse('get_transaction_sum', kwargs={'transaction_id': self.transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('sum', response.json())

    def test_has_dependents(self):
        url = reverse('has_dependents', kwargs={'transaction_id': self.transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('has_children', response.json())

    def test_get_potential_parents(self):
        url = reverse('potential_parents', kwargs={'transaction_id': self.transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assuming potential parents are all transactions for this test case
        self.assertIn(self.transaction.id, response.json())

    def test_reassign_children(self):
        child_transaction = Transaction.objects.create(user=self.user, amount=500, type='debit', parent=self.transaction)
        url = reverse('reassign_children', kwargs={'transaction_id': self.transaction.id})
        response = self.client.put(url, {"parent": None}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')