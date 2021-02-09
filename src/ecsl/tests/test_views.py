from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from datetime import datetime, date
from django.urls import reverse, reverse_lazy
from django.utils.timezone import get_current_timezone
from .shared_methods import create_user, create_eventECSL, not_logged_in_user, create_payment, create_package, \
    create_payment_option, create_inscription as create_event_inscription
from ecsl.models import EventECSL, Inscription, Encuentros_Anteriores, Gustos, Package, Payment, PaymentOption
from django.core.files.uploadedfile import SimpleUploadedFile

USER_NAME = 'test2'
USER_EMAIL = 'test2@mail.com'
PASSWORD = 'testtest2'


def create_encuentros_anteriores():
    return Encuentros_Anteriores.objects.create(name="ECSL Test")


def create_gustos():
    return Gustos.objects.create(name="Gusto Test")


def create_paypal_option(event):
    return PaymentOption.objects.create(name="Paypal", identification="Paypal", tipo="Paypal", email='paypal@gmail.com',
                                        event=event)


def create_paypal_payment(user, event, package, option):
    return Payment.objects.create(option=option, user=user, confirmado=True, event=event, package=package)


def create_inscription(self):
    return self.client.post(reverse('create_profile'), data={
        'first_name': 'Tester',
        'last_name': 'Testing',
        'identification': '11230456',
        'direccion_en_su_pais': 'San José, Costa Rica',
        'nationality': 'Costa Rica',
        'gender': 'Masculino',
        'camiseta': 'M',
        'born_date': '2000-01-01',
        'institution': 'UCR',
        'encuentros': self.encuentros.pk,
        'alimentary_restriction': 'Ninguna',
        'health_consideration': 'Ninguna',
        'gustos_manias': self.gustos.pk,
        'observacion_gustos_manias': 'Ninguna',
        'comentario_general': 'Ninguno',
        'aparecer_en_participantes': 1,
    })


class CreateProfileTest(TestCase):
    """
        This view displays a form to get registered as an event participant. The user has to fill this form with
        his/her personal information. Once the form is submitted, the data is recorded in the database and the
        user is taken as an event participant. The user should get redirected to the main page after the form submitting.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.gustos = create_gustos()
        self.encuentros = create_encuentros_anteriores()

    def test_create_profile(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('create_profile'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        inscriptions = Inscription.objects.filter(user=self.user).count()
        self.assertEqual(inscriptions, 0)

        response = create_inscription(self)
        self.assertRedirects(response, reverse('index'))

        inscriptions = Inscription.objects.filter(user=self.user).count()
        self.assertEqual(inscriptions, 1)
        Inscription.objects.filter(user=self.user).delete()

    def test_create_profile_not_logged_in_user(self):
        target = '/register/profile/create'
        redirect_to = '/accounts/login/?next=/register/profile/create'
        not_logged_in_user(self, target, redirect_to)

    def test_create_profile_empty_form(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('create_profile'))  # Posting an empty form
        self.assertEqual(response.status_code, HTTPStatus.OK)
        inscriptions = Inscription.objects.filter(user=self.user).count()  # Checking no inscription were created
        self.assertEqual(inscriptions, 0)

    def test_create_profile_no_active_event(self):
        EventECSL.objects.filter(pk=self.event.pk).update(current=False)
        self.client.login(username=USER_NAME, password=PASSWORD)

        response = create_inscription(self)
        inscriptions = Inscription.objects.filter(user=self.user).count()  # Checking no inscription were created
        # inscriptions 0 due to user should not be able to register for an event that does not exist
        self.assertEqual(inscriptions, 0)
        self.assertRedirects(response, reverse('no-events'))

        Inscription.objects.filter(user=self.user).delete()
        EventECSL.objects.filter(pk=self.event.pk).update(current=True)

    def test_create_profile_existing_profile(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = create_inscription(self)
        response = self.client.get(reverse('create_profile'))
        profile = Inscription.objects.filter(user=self.user).first()
        self.assertRedirects(response, reverse('edit_profile', args=(profile.pk,)))

        Inscription.objects.filter(user=self.user).delete()


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
        self.assertRedirects(response, reverse('create_payment'))
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
        self.assertEqual(response.status_code, 200)


