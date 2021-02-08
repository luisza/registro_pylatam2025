from django.contrib.messages import get_messages
from proposal.models import BlockSchedule, Speech, Topic, SpeechType, Room, SpeechSchedule
import datetime

from proposal.forms import TypeForm

x = datetime.datetime(2020, 5, 17)

from datetime import datetime
import datetime
from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ecsl.models import EventECSL, Inscription, Payment, PaymentOption, Package, Becas

import tempfile


class TestBecas(TestCase):

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

        self.inscription = Inscription(user=self.user,
                                       status=2,
                                       gender='Masculino',
                                       nationality='Costa Rica',
                                       identification='123456789',
                                       direccion_en_su_pais='San Jose',
                                       born_date=datetime.datetime(1997, 8, 14),
                                       institution='Solvo',
                                       event=self.event)

        self.paymentOption = PaymentOption(name='PagoOption',
                                           tipo='Deposito',
                                           email='email@mail.com')

        self.package = Package(name='Package',
                               description='Description',
                               price=5.00)

        self.payment = Payment(user=self.user,
                               confirmado=True,
                               event=self.event,
                               option=self.paymentOption,
                               package=self.package)

        self.becas = Becas(user=self.user,
                           razon='none',
                           aportes_a_la_comunidad='none',
                           tiempo='1 month',
                           observaciones='no',
                           estado=2,
                           event=self.event)

    # Becas Detail
    # BeD1
    def test_becas_Detail(self):
        self.event.save()
        self.user.save()
        self.becas.save()
        self.cliente.login(username='daniel', password='daniel')
        url = '/becas/detail/' + str(self.becas.pk)
        response = self.cliente.get(url)
        self.assertEqual(response.status_code, 200)

    # BeD2
    def test_becas_Detail_user_not_loggin(self):
        self.event.save()
        self.user.save()
        self.becas.save()
        url = '/becas/detail/' + str(self.becas.pk)
        response = self.cliente.get(url)

        url = '/accounts/login/?next=' + url
        self.assertRedirects(response, url, status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    # BeD3
    def test_becas_Detail_no_Event(self):
        self.event.current = False
        self.event.save()
        self.user.save()
        self.becas.save()
        self.cliente.login(username='daniel', password='daniel')
        url = '/becas/detail/' + str(self.becas.pk)
        response = self.cliente.get(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        url = reverse('index')
        self.assertRedirects(response, url, status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertEqual(messages[0], 'Lo lamentamos, pero la solicitud de beca que está buscando no existe')

    # BeD4
    def test_becas_Detail_no_scholarship(self):
        self.event.save()
        self.user.save()
        self.becas.save()
        User.objects.create_user(username='Luis',
                                 email='Luis@mail.com',
                                 password='Luis')
        self.cliente.login(username='Luis', password='Luis')
        url = '/becas/detail/' + str(self.becas.pk)
        response = self.cliente.get(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        url = reverse('index')
        self.assertRedirects(response, url, status_code=302, target_status_code=200,
                             fetch_redirect_response=False)
        self.assertEqual(messages[0], 'Lo lamentamos, pero la solicitud de beca que está buscando no existe')