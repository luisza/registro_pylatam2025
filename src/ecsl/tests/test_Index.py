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
from ecsl.views import Index

import tempfile


class TestIndex(TestCase):

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

        self.topic = Topic(name='Artificial Inteligence',
                           color='#cccccc',
                           event=self.event)

        self.speechType = SpeechType(name='Conversatory',
                                     time=60,
                                     event=self.event,
                                     is_special=False)

        self.speech = Speech(user=self.user,
                             speaker_information='AI expert',
                             title='Deep Learning',
                             description='Deep learning Algorithms',
                             topic=self.topic,
                             audience='everybody',
                             notes='Nope',
                             speech_type=self.speechType,
                             event=self.event,
                             is_scheduled=True)

    # Ind1
    def test_index(self):
        self.event.beca_start = datetime.datetime(2021, 1, 15)
        self.event.beca_end = datetime.datetime(2021, 12, 15)
        self.event.save()
        self.becas.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        self.cliente.login(username='daniel', password='daniel')
        current_event = EventECSL.objects.filter(current=True).first()
        response = self.cliente.get(reverse('index'))
        self.assertEqual(response.context['becas_period'], current_event.is_beca_active)
        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    # Ind2
    def test_index_no_checking_period(self):
        self.event.save()
        self.becas.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        self.cliente.login(username='daniel', password='daniel')
        current_event = EventECSL.objects.filter(current=True).first()
        response = self.cliente.get(reverse('index'))
        self.assertTrue(response.context['becas_period'])
        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    # Ind3
    def test_index_not_logged(self):
        self.event.start_date = datetime.datetime(2020, 1, 15)
        self.event.end_date = datetime.datetime(2019, 1, 15)
        self.event.save()

        self.becas.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        current_event = EventECSL.objects.filter(current=True).first()
        response = self.cliente.get(reverse('index'))
        self.assertNotIn('beca', response.context)
        self.assertNotIn('becas_period', response.context)
        self.assertNotIn('speech_url', response.context)

        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    # Ind5
    def test_index_no_proposal(self):
        self.event.beca_start = datetime.datetime(2021, 1, 15)
        self.event.beca_end = datetime.datetime(2021, 12, 15)
        self.event.save()
        self.becas.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        self.cliente.login(username='daniel', password='daniel')
        current_event = EventECSL.objects.filter(current=True).first()
        response = self.cliente.get(reverse('index'))
        self.assertNotIn('speech_url', response.context)
        self.assertEqual(response.context['becas_period'], current_event.is_beca_active)
        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    # Ind6
    def test_index_2_events(self):
        self.event.beca_start = datetime.datetime(2021, 1, 15)
        self.event.beca_end = datetime.datetime(2021, 12, 15)
        self.event.save()
        event2 = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".png").name,
                           location='Nicaragua',
                           description='Second Event',
                           start_date=datetime.datetime(2022, 1, 15),
                           end_date=datetime.datetime(2023, 1, 15),
                           current=True,
                           start_date_proposal=datetime.datetime(2022, 1, 15),
                           end_date_proposal=datetime.datetime(2023, 1, 15))
        event2.save()
        self.becas.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        self.cliente.login(username='daniel', password='daniel')
        current_event = EventECSL.objects.filter(current=True).first()
        second_current_event = EventECSL.objects.filter(current=True, location='Nicaragua').first()
        response = self.cliente.get(reverse('index'))
        self.assertEqual(response.context['becas_period'], current_event.is_beca_active)
        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertNotEqual(response.context['event_name'], str(second_current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertNotEqual(response.context['event_logo'], second_current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertNotEqual(response.context['event_location'], second_current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertNotEqual(response.context['event_description'], second_current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})