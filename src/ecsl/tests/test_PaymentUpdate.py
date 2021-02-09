from http import HTTPStatus
from django.test import TestCase, Client
from .shared_methods import create_user, create_eventECSL, not_logged_in_user, create_payment, create_package, \
    create_payment_option, create_paypal_option, create_paypal_payment
from ecsl.models import EventECSL, Inscription, Encuentros_Anteriores, Gustos, Package, Payment, PaymentOption
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

USER_NAME = 'test2'
USER_EMAIL = 'test2@mail.com'
PASSWORD = 'testtest2'


class PaymentUpdateTest(TestCase):
    """
        This view displays a form with the detail of an already done payment. While the payment is not marked as
        confirmed, changes to it should be allowed.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.payment_option = create_payment_option(self.event)
        self.package = create_package(self.event)
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)

    def test_payment_update(self):
        temp_payment_option = PaymentOption.objects.create(name="Temporal",
                                                           identification='654321',
                                                           tipo='Transferencia',
                                                           email='ejemploSinpe2@mail.com',
                                                           event=self.event)
        temp_package = Package.objects.create(name='Básico',
                                              description='Transporte y alimentación',
                                              price=15,
                                              event=self.event)

        self.client.login(username=USER_NAME, password=PASSWORD)
        Payment.objects.filter(user=self.user.pk).update(confirmado=False)
        response = self.client.get(reverse('edit_payment', kwargs={'pk': self.payment.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        invoice_file = SimpleUploadedFile("invoice.pdf", b"file_content", content_type="video/pdf")
        response = self.client.post(reverse('edit_payment', kwargs={'pk': self.payment.pk}), data={
            'package': temp_package.pk,
            'option': temp_payment_option.pk,
            'codigo_de_referencia': '1122',
            'invoice': invoice_file
        })
        self.assertRedirects(response, reverse('index'))

        payment = Payment.objects.filter(user=self.user).first()
        self.assertEqual(payment.package, temp_package)
        self.assertEqual(payment.option, temp_payment_option)
        self.assertEqual(payment.codigo_de_referencia, '1122')
        payment.delete()
        temp_package.delete()
        temp_payment_option.delete()
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)

    def test_payment_update_not_logged_in_user(self):
        target = '/registro/update/' + str(self.payment.pk)
        redirect_to = '/accounts/login/?next=/registro/update/' + str(self.payment.pk)
        not_logged_in_user(self, target, redirect_to)

    def test_payment_update_no_payment_registered(self):
        """
            If the user does not have a payment made to edit, the user should get redirected to the payment creation page.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        self.payment.delete()
        response = self.client.get(reverse('edit_payment', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, 404)
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)

    def test_payment_update_no_event(self):
        """
            When there is no active event, the user should get redirected to the no-events page.
        """
        EventECSL.objects.filter(pk=self.event.pk).update(current=False)
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('edit_payment', kwargs={'pk': 0}))
        self.assertRedirects(response, reverse('no-events'))

    def test_payment_update_empty_form(self):
        """
             When user submits a form with blanks, the data is not updated and the user is alerted that there
             are spaces left to be filled.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('edit_payment', kwargs={'pk': self.payment.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)  # It means that the user is not being redirected

    def test_payment_update_paypal_confirmed_other_option(self):
        """
            When a payment done using PayPal is confirmed, payment update with another option must not be allowed.
            Instead, the user should get redirected to the main page in order to avoid double payments.
        """
        paypal_option = create_paypal_option(self.event)
        paypal_payment = create_paypal_payment(self.user, self.event, self.package, paypal_option)
        invoice_file = SimpleUploadedFile("invoice.pdf", b"file_content", content_type="video/pdf")

        self.payment.delete()
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('edit_payment', kwargs={'pk': paypal_payment.pk}), data={
            'package': self.package.pk,
            'option': self.payment_option.pk,
            'codigo_de_referencia': '0098',
            'invoice': invoice_file
        })
        self.assertRedirects(response, reverse('index'))

        payment = Payment.objects.filter(user=self.user).first()
        self.assertNotEqual(payment.option, self.payment_option)
        self.assertRedirects(response, reverse('index'))

        paypal_payment.delete()
        paypal_option.delete()
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)

    def test_payment_update_confirmed_payment(self):
        """
            The user should not be able to update any information about the confirmed payment. The user should be
            redirected to the index.
        """
        invoice_file = SimpleUploadedFile("invoice.pdf", b"file_content", content_type="video/pdf")

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('edit_payment', kwargs={'pk': self.payment.pk}), data={
            'package': self.package.pk,
            'option': self.payment_option.pk,
            'codigo_de_referencia': '1133',
            'invoice': invoice_file
        })

        self.assertRedirects(response, reverse('index'))
        self.assertNotEqual(self.payment.codigo_de_referencia, '1133')
