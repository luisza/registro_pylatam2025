from django.contrib.auth.models import User
from django.test import Client, TestCase

from ecsl.models import Payment, PaymentOption
from ecsl.tests.general_set_up import GeneralSetUp


class PaymentDoneTestCase(GeneralSetUp, TestCase):
    test_client = None
    user = None

    def setUp(self):
        self.current_event = self.create_event()
        self.user = User.objects.create(username='userexample')
        self.user.set_password('password')
        self.user.save()
        self.test_client = Client()
        self.test_client.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)

    def test_access_to_payment_done_through_url(self):
        """
            If an user tries to access to the payment_done page through url, the system denies access
        """
        response = self.test_client.get('/payment-done')
        try:
            self.assertRedirects(response, '/payment-done/', status_code=301)
        except Exception as e:
            self.assertIsNotNone(e)

    def test_payment_done(self):
        """
            Checking the correct access to payment done page after an user pay the inscription through paypal
        """
        p_Option = PaymentOption.objects.filter(name='Paypal').first()
        self.create_payment(user=self.user, event=self.current_event,
                            package=self.create_package(event=self.current_event),
                            option=p_Option)
        response = self.test_client.get('/payment-done', follow=True)
        self.assertEqual(Payment.objects.all().first().confirmado, True)
        self.assertRedirects(response, '/payment-done/', status_code=301)


    def test_payment_done_two_current_event(self):
        """
            Checking the correct access to payment done page after an user pay the inscription through paypal
        """
        self.create_event()
        p_Option = PaymentOption.objects.filter(name='Paypal').first()
        self.create_payment(user=self.user, event=self.current_event,
                                      package=self.create_package(event=self.current_event),
                                      option=p_Option)
        response = self.test_client.get('/payment-done', follow=True)
        self.assertEqual(Payment.objects.all().first().confirmado, True)
        self.assertRedirects(response, '/payment-done/', status_code=301)
        self.assertEqual(Payment.objects.all().first().event, self.current_event)
