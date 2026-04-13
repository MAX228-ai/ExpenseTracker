from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Transaction
import datetime


class TransactionCreateTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testlietotajs',
            password='StipraParole123!'
        )
        self.client.login(username='testlietotajs', password='StipraParole123!')
        self.url = reverse('transaction_create')

    def test_create_transaction_success(self):
        payload = {
            'amount': '75.50',
            'category': Transaction.Category.FOOD,
            'date': datetime.date.today().isoformat(),
            'description': 'Iepirkšanās veikalā',
        }
        response = self.client.post(self.url, data=payload)

        self.assertRedirects(response, reverse('transaction_list'))
        self.assertEqual(Transaction.objects.count(), 1)

        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.amount, Decimal('75.50'))
        self.assertEqual(transaction.category, Transaction.Category.FOOD)
        self.assertEqual(transaction.description, 'Iepirkšanās veikalā')

    def test_create_transaction_negative_amount_fails(self):
        payload = {
            'amount': '-50.00',
            'category': Transaction.Category.OTHER,
            'date': datetime.date.today().isoformat(),
            'description': 'Negatīva summa',
        }
        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertFormError(
            response, 'form', 'amount',
            'Summai jābūt lielākai par nulli.'
        )


class UnauthorizedAccessTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('transaction_list')

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.url}')

    def test_authenticated_user_can_access_list(self):
        User.objects.create_user(username='autlietotajs', password='Parole123!')
        self.client.login(username='autlietotajs', password='Parole123!')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')