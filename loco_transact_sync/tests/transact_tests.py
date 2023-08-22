from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Transaction
from rest_framework.test import APIClient

class TransactionTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_create_transaction(self):
        url = reverse('create_transaction')
        data = {'amount': 100, 'type': 'expense'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('transaction_id', response.data)

    def test_all_transaction_ids(self):
        Transaction.objects.create(user=self.user, amount=100, type='expense')
        url = reverse('all_transaction_ids')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_transaction_detail_get(self):
        transaction = Transaction.objects.create(user=self.user, amount=100, type='expense')
        url = reverse('transaction_detail', kwargs={'transaction_id': transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_transaction_detail_put(self):
        transaction = Transaction.objects.create(user=self.user, amount=100, type='expense')
        url = reverse('transaction_detail', kwargs={'transaction_id': transaction.id})
        data = {'amount': 150, 'type': 'expense'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_transaction(self):
        transaction = Transaction.objects.create(user=self.user, amount=100, type='expense')
        url = reverse('delete_transaction', kwargs={'transaction_id': transaction.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_get_transaction_by_type(self):
        # Create a sample transaction
        Transaction.objects.create(user=self.user, type="testType", amount=100)
        response = self.client.get('/path-to-get_transaction_by_type/testType/')  # Update the path
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_get_transaction_sum(self):
        trans = Transaction.objects.create(user=self.user, type="testType", amount=100)
        response = self.client.get(f'/path-to-get_transaction_sum/{trans.id}/')  # Update the path
        self.assertEqual(response.status_code, 200)
        self.assertTrue("sum" in response.json())

    def test_has_dependents(self):
        parent_trans = Transaction.objects.create(user=self.user, type="testType", amount=100)
        child_trans = Transaction.objects.create(user=self.user, type="testType", amount=50, parent=parent_trans)
        response = self.client.get(f'/path-to-has_dependents/{parent_trans.id}/')  # Update the path
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["has_children"])

    def test_get_potential_parents(self):
        trans = Transaction.objects.create(user=self.user, type="testType", amount=100)
        response = self.client.get(f'/path-to-get_potential_parents/{trans.id}/')  # Update the path
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_reassign_children(self):
        parent_trans1 = Transaction.objects.create(user=self.user, type="testType", amount=100)
        parent_trans2 = Transaction.objects.create(user=self.user, type="testType", amount=150)
        child_trans = Transaction.objects.create(user=self.user, type="testType", amount=50, parent=parent_trans1)
        data = {'parent': parent_trans2.id}
        response = self.client.put(f'/path-to-reassign_children/{child_trans.id}/', data)  # Update the path
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")