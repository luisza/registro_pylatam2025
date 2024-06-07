from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ecsl.models import Payment
from ecsl.tests.general_set_up import GeneralSetUp


class CreateRegisterTestCase(GeneralSetUp, TestCase):

    user = None
    cliente = None
    invoice_file = None
    payment = None

    def setUp(self):
        self.current_event = self.create_event()
        self.user = User.objects.create(username='userexample')
        self.user.set_password('password')
        self.user.save()
        self.cliente = Client()

        self.invoice_file = SimpleUploadedFile("invoice.pdf", b"file_content", content_type="video/pdf")
        self.payment = {
            "package": self.create_package(event=self.current_event).pk,
            "option": self.create_payment_option(event=self.current_event).pk,
            "invoice": self.invoice_file,
            "codigo_de_referencia": "111111",
        }

    def test_createRegister(self):
        """
            This test help us to check is a payment is saved through createRegister view
        """
        self.cliente.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)
        self.cliente.post(reverse('create_payment'), self.payment)
        self.assertGreater(len(Payment.objects.all()), 0)

    def test_createRegister_twice_one_event(self):
        """
            The code below checking that we can't pay more than one inscription per event
        """
        self.cliente.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)
        self.cliente.post(reverse('create_payment'), self.payment)
        self.cliente.post(reverse('create_payment'), self.payment)
        response = self.cliente.post(reverse('create_payment'), self.payment)
        self.assertEqual(len(Payment.objects.all()), 1)
        self.assertIsNone(response.context.get('message'))

    def test_createRegister_event_without_spaces(self):
        """
            The code below checking that we can't pay an inscription when the event does not have spaces available.
        """
        self.current_event.max_inscription = 1
        self.current_event.save
        self.cliente.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)
        response = self.cliente.post(reverse('create_payment'), self.payment, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertTrue('Felicidades su registro se ha completado satisfactoriamente, por favor regístrese en las charlas'
                        in message.message)
        self.cliente.logout()
        second_user = User.objects.create(username='userexample2')
        second_user.set_password('password')
        second_user.save()
        self.cliente.login(username="userexample2", password='password')
        self.create_inscription(event=self.current_event, user=second_user)
        response = self.cliente.post(reverse('create_payment'), self.payment, follow=True)
        self.assertEqual(list(response.context['messages']), [])
        self.assertEqual(len(Payment.objects.all()), 1)

    def test_createRegister_with_out_event(self):
        """
            This test help us to check that we can't pay an inscription without a current event
        """
        self.current_event.current = False
        self.current_event.save()
        self.cliente.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)
        response = self.cliente.post(reverse('create_payment'), self.payment, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertTrue(
            'Lo sentimos, pero no hay evento para que se pueda registrar'
            in message.message)