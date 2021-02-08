from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from datetime import datetime, date
from django.urls import reverse, reverse_lazy
from django.utils.timezone import get_current_timezone
from .shared_methods import create_user, create_eventECSL, not_logged_in_user, create_payment, create_package, \
    create_payment_option, create_inscription as create_event_inscription, create_paypal_option, create_paypal_payment
from ecsl.models import EventECSL, Inscription, Encuentros_Anteriores, Gustos, Package, Payment, PaymentOption

USER_NAME = 'test2'
USER_EMAIL = 'test2@mail.com'
PASSWORD = 'testtest2'


class ProcessPaymentTest(TestCase):
    """
        When making the event inscription payment via PayPal, this view displays the package's name and its description.
        Below, the user can find a "Buy Now" button that leads to the PayPal page to proceed with the payment.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.package = create_package(self.event)
        self.event = create_eventECSL()
        self.inscription = create_event_inscription(self.user, self.event)
        self.paypal_option = create_paypal_option(self.event)
        self.payment_option = create_payment_option(self.event)
        Payment.objects.filter(user=self.user.pk).delete()

    def test_process_payment(self):
        """
            The page is displayed with the package information.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['price'].name, self.package.name)
        self.assertEqual(response.context['price'].price, self.package.price)

    def test_process_payment_not_logged_in_user(self):
        """
            This page should not be allowed for accessing to not logged in users. They should be redirected to the login
            page.
        """
        target = '/process-payment/' + self.package.name
        redirect_to = '/accounts/login/?next=' + target
        not_logged_in_user(self, target, redirect_to)

    def test_process_payment_invalid_package_name(self):
        """
            Entering a non-existent package name in the URL should result in a redirection to the index page.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': 'InvalidPackageName'}))
        self.assertRedirects(response, reverse('index'))

    def test_process_payment_paypal_payment_confirmed(self):
        """
            Since multiple payments should not be allowed, the users should get redirected to the index page
            when there is a PayPal payment done associated with them.
        """
        paypal_payment = create_paypal_payment(self.user, self.event, self.package, self.paypal_option)
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertRedirects(response, reverse('index'))
        paypal_payment.delete()

    def test_process_payment_paypal_payment_not_confirmed(self):
        """
            Since the PayPal payment was not completed, the payment process should be able to continue.
        """
        paypal_payment = create_paypal_payment(self.user, self.event, self.package, self.paypal_option)
        paypal_payment.confirmado = False
        paypal_payment.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        paypal_payment.delete()

    def test_process_payment_no_paypal_payment_confirmed(self):
        """
            Since there is a confirmed payment, the user must be redirected to the index in order to avoid multiple
            payment problems.
        """
        payment = create_payment(self.user, self.payment_option, self.event, self.package)

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertRedirects(response, reverse('index'))

    def test_process_payment_no_paypal_payment_not_confirmed(self):
        """
            If the user has done a payment using any other option than PayPal, the user must be redirected to the index
            page although the payment is not confirmed, this is just to avoid multiple payment problems.
        """
        payment = create_payment(self.user, self.payment_option, self.event, self.package)
        payment.confirmado = False
        payment.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertRedirects(response, reverse('index'))

        payment.delete()

    def test_process_payment_no_inscription(self):
        """
            If an user tries to reach this view and he has no inscription, this page must not be shown and the user must
            be redirected to the main page instead, asking for the necessary inscription.
        """
        self.inscription.delete()
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertRedirects(response, reverse('index'))
        self.inscription = create_event_inscription(self.user, self.event)

    def test_process_payment_free_package(self):
        """
            Since PayPal does not accept $0 charges, the user must not reach the PayPal page but be redirected to the
            index page. The user’s payment must be recorded into the database and it has to be marked as confirmed.
        """
        self.package.price = 0
        self.package.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('process_payment', kwargs={'text': self.package.name}))
        self.assertRedirects(response, reverse('index'))

        payment = Payment.objects.filter(user=self.user, package=self.package).count()
        self.assertEqual(payment, 1)
        Payment.objects.filter(user=self.user, package=self.package).delete()
        self.package.price = 50
        self.package.save()
