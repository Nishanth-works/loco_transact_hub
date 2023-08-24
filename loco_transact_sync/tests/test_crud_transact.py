# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Transaction
from django.urls import reverse

class TransactionAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('user1', 'user1@example.com', 'password')
        self.client.force_authenticate(user=self.user)
        self.transaction = Transaction.objects.create(user=self.user, amount=1000, type='credit')

    def test_create_transaction(self):
        url = reverse('create_transaction')
        data = {'amount': 500, 'type': 'debit'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')

    def test_all_transaction_ids(self):
        url = reverse('all_transaction_ids')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.transaction.id, response.json())

    def test_transaction_detail(self):
        url = reverse('transaction_detail', kwargs={'transaction_id': self.transaction.id})
        
        # Testing GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('id'), self.transaction.id)

        # Testing PUT
        updated_data = {'amount': 1200, 'type': 'debit'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')

    def test_delete_transaction(self):
        # First create a transaction to delete
        transaction = Transaction.objects.create(user=self.user, amount=1000, type='debit')
        url = reverse('delete_transaction', kwargs={'transaction_id': transaction.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'deleted')