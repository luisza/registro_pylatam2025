from django.test import TestCase, Client
from django.urls import reverse
from .shared_methods import create_user

USER_NAME = 'test2'
USER_EMAIL = 'test2@mail.com'
PASSWORD = 'testtest2'


class PaymentCancelledTest(TestCase):
    """
        The view is shown when a PayPal payment is cancelled.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)

    def test_payment_cancelled(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('payment_cancelled'))
        self.assertRedirects(response, reverse('index'))
