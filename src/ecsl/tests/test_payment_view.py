from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from ecsl.models import Payment
from ecsl.tests.general_set_up import GeneralSetUp


class PaymentViewTestCase(GeneralSetUp, TestCase):
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

    def test_paymentView_no_paid(self):
        """
            This test check if the system redirect to the expected page, in this case the user has not been paid
             the inscription so he will be redirect to the create payment page.
        """
        respose = self.test_client.post(reverse('payment'))
        self.assertRedirects(respose, '/registro/create', status_code=302)

    def test_paymentView_has_a_payment(self):
        """
            This test check if the system redirect to the expected page, in this case the user has been paid
             an inscription, so he will be redirect to the update payment page.
        """
        self.create_payment(user=self.user, event=self.current_event,
                            package=self.create_package(event=self.current_event),
                            option=self.create_payment_option(event=self.current_event))
        respose = self.test_client.post(reverse('payment'))
        self.assertRedirects(respose, "/registro/update/{}".format(Payment.objects.all().first().id), status_code=302)

    def test_paymentView_not_event(self):
        """
            If an user tries to go to register module and the system does not has a current event it denies the access
            an redirect to sineventos page
        """
        self.current_event.current = False
        self.current_event.save()
        response = self.test_client.get('/registro')
        response = self.test_client.get(response.url)
        self.assertRedirects(response, "/sineventos/", status_code=302)

    def test_paymentView_no_logged(self):
        """
            If an user tries to go to register module through ulr and hes is not already logged the system redirec to
            to log in page
        """
        self.current_event.current = True
        self.current_event.save()
        self.test_client.logout()
        response = self.test_client.get('/registro')
        self.assertRedirects(response, "/accounts/login/?next=/registro", status_code=302)