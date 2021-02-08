from ecsl import views
from django.contrib.messages import get_messages
from proposal.models import BlockSchedule, Speech, Topic, SpeechType, Room, SpeechSchedule
import datetime
from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ecsl.models import EventECSL, Inscription, Payment, PaymentOption, Package, Becas
from ecsl.views import Index, CustomContactFormCaptcha, contact

import tempfile
from django.test import TestCase, Client, RequestFactory, override_settings

class TestContact(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='daniel',
                                             email='daniel@mail.com',
                                             password='daniel')
        self.event = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Panama',
                               description='description',
                               start_date=datetime.datetime(2021, 1, 15),
                               end_date=datetime.datetime(2022, 1, 15),
                               current=True,
                               start_date_proposal=datetime.datetime(2021, 1, 15),
                               end_date_proposal=datetime.datetime(2022, 1, 15))

    # contact-us

    # COU1 F
    def test_contact_us_logged_In(self):
        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.get(reverse('contact-us'))
        self.assertEqual(response.context['form']['Name'].value(), 'daniel')
        self.assertEqual(response.context['form']['Email'].value(), 'daniel@mail.com')

    # COU2 F
    def test_contact_us_not_logged_In(self):
        response = self.cliente.get(reverse('contact-us'))
        self.assertNotEqual(response.context['form']['Name'].value(), 'daniel')
        self.assertNotEqual(response.context['form']['Email'].value(), 'daniel@mail.com')

    # Contact

    # Con1
    def test_contact(self):
        data = {'Name': 'Daniel',
                'Email': 'daniel@gmail.com',
                'Subject': 'Troubles',
                'Message': 'Message',
                'captcha_0': "8e10ebf60c5f23fd6e6a9959853730cd69062a15",
                'captcha_1': "passed",
                }

        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.post(reverse('contact'), data, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0], 'Gracias! Mensaje enviado con éxito')
        self.assertTemplateUsed(response, 'contact/contact_us.html')

    # Con2
    def test_contact_anothermail(self):
        data = {'Name': 'Daniel',
                'Email': 'dano@gmail.com',
                'Subject': 'Troubles',
                'Message': 'Message',
                'captcha_0': "8e10ebf60c5f23fd6e6a9959853730cd69062a15",
                'captcha_1': "passed",
                }

        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.post(reverse('contact'), data, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0], 'Gracias! Mensaje enviado con éxito')
        self.assertTemplateUsed(response, 'contact/contact_us.html')

    # Con3
    def test_contact_get(self):
        response = self.cliente.get(reverse('contact'))
        self.assertRedirects(response, reverse('contact-us'), status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    # Con4
    def test_contact_Invalid(self):
        data = {'Name': 'Daniel',
                'Email': 'dano@gmail.com',
                'subject': 'Troubles',
                'Message': 'Message'}
        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.post(reverse('contact'), data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0], 'Captcha inválido, intente de nuevo')
        self.assertTemplateUsed(response, 'contact/contact_us.html')

    # Con5
    def test_contact(self):
        data = {'Name': 'Daniel',
                'Email': 'daniel@gmail.com,daniel@gmail.com',
                'Subject': 'Troubles',
                'Message': 'Message',
                'captcha_0': "8e10ebf60c5f23fd6e6a9959853730cd69062a15",
                'captcha_1': "passed",
                }

        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.post(reverse('contact'), data, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(messages[0], 'Gracias! Mensaje enviado con éxito')
        self.assertTemplateUsed(response, 'contact/contact_us.html')