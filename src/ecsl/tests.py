"""
    This is  module that help us to check some test about ecsl app.

    Test Case on this module:
        - CharlasTestCase:
            On CharlasTestCase we can find some test functions
                - test_agenda_days_list
                - test_agenda_not_event
                - test_block_schedule
"""

from proposal.models import BlockSchedule, Speech, Topic, SpeechType, Room, SpeechSchedule
import datetime

x = datetime.datetime(2020, 5, 17)

from datetime import datetime
import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import EventECSL, Inscription, Payment, PaymentOption, Package, Becas
from .views import Index

import tempfile


class TestViews(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.user = User.objects.create_user(username='daniel', email='daniel@mail.com', password='daniel')
        self.event = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Panama',
                               description='description',
                               start_date=datetime.datetime(2021, 1, 15),
                               end_date=datetime.datetime(2021, 1, 15),
                               current=True,
                               start_date_proposal=datetime.datetime(2021, 1, 15),
                               end_date_proposal=datetime.datetime(2021, 1, 15))

        self.inscription = Inscription(user=self.user,
                                       status=2,
                                       gender='Masculino',
                                       nationality='Costa Rica',
                                       identification='123456789',
                                       direccion_en_su_pais='San Jose',
                                       born_date=datetime.datetime(1997, 8, 14),
                                       institution='Solvo')

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
                           tiempo='1 mes',
                           observaciones='no',
                           estado=2,
                           event=self.event)

    def test_index_no_event(self):
        request = self.cliente.get(reverse('index'))
        response = Index.as_view()(request)

        self.assertRedirects(response, '/sineventos/', status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_index_with_event(self):
        self.event.save()
        response = self.cliente.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_index_context(self):
        self.event.save()
        self.user.save()
        self.inscription.save()
        self.package.save()
        self.paymentOption.save()
        self.payment.save()
        response = self.cliente.get(reverse('index'))
        current_event = EventECSL.objects.filter(current=True).first()

        self.assertEqual(response.context['event_name'], str(current_event))
        self.assertEqual(response.context['event_logo'], current_event.logo)
        self.assertEqual(response.context['event_location'], current_event.location)
        self.assertEqual(response.context['event_description'], current_event.description)
        self.assertEqual(response.context['numparticipantes'], 1)
        self.assertEqual(response.context['genero'], {'masculino': 1, 'femenino': 0, 'otro': 0})

    def test_contact(self):
        response = self.cliente.get(reverse('contact'))
        self.assertRedirects(response, reverse('contact-us'), status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    def test_contact_form(self):
        response = self.cliente.post(reverse('contact'), {'name': 'daniel','email':'daniel@mail.com', 'subject': 'something' ,'message':'message'})
        self.assertEqual(response.status_code,200)

class CharlasTestCase(TestCase):

    days_list = None

    def setUp(self):
        """
            Lista of days form start_date to end_date in an event
        """
        self.days_list = [datetime.date(2021, 1, 10), datetime.date(2021, 1, 11),
                          datetime.date(2021, 1, 12), datetime.date(2021, 1, 13),
                          datetime.date(2021, 1, 14), datetime.date(2021, 1, 15)]


    topic = {
        'name': 'mytopic',
        'color': 'red',

    }

    speech_type = 'speech'

    room = {
        'name': 'myroom',
        'spaces': 30,
        'map': 'map.jpg'
    }

    user = {
        'username': 'userexample',
        'email': 'user@example.com',
        'password': 'password',
    }

    event = {

        'logo': 'logo.png',
        'start_date': datetime.datetime(2021, 1, 10),
        'end_date': datetime.datetime(2021, 1, 15),
        'location': 'San Jose, Costa Rica',
        'description': 'esta es mi prueba',
        'current': True,
        'organizer1': 'Juanito Perez Rondo',
        'organizer2': 'Carla Matus Ruiz',
        'certificate_Header': 'header.png',
        'certificate_Footer': 'footer.png',
        'phone_event': '0000000',
        'start_date_proposal': datetime.datetime(2020, 5, 17),
        'end_date_proposal': datetime.datetime(2020, 5, 17),
        'email_event': 'test@example.com',
        'beca_start': datetime.datetime(2020, 5, 17),
        'beca_end': datetime.datetime(2020, 5, 17),
        'max_inscription': 3,

    }

    activity = {

        'user': None,
        'speaker_information': 'profesor',
        'title': 'Testing',
        'description': 'description',
        'topic': 'testing',
        'audience': 'audiencia',
        'skill_level': 1,
        'notes': 'pc',
        'speech_type': None,
        'presentation': 'presentation',
        'event': None,

    }

    speech_schedule = {

        'start_time': datetime.datetime(2021, 1, 11),
        'end_time': datetime.datetime(2021, 1, 11),
        'speech': None,
        'room': None,
    }

    block_schedule = {

        'start_time': datetime.datetime(2021, 1, 11),
        'end_time': datetime.datetime(2021, 1, 11),
        'is_speech': True,
        'text': 'texto block',
        'color': 'red',

    }

    def create_event(self):
        return EventECSL.objects.create(logo=self.event['logo'], start_date=self.event['start_date'],
                                        end_date=self.event['end_date'], location=self.event['location'],
                                        description=self.event['description'], current=self.event['current'],
                                        organizer1=self.event['organizer1'], organizer2=self.event['organizer2'],
                                        certificate_Header=self.event['certificate_Header'],
                                        certificate_Footer=self.event['certificate_Footer'],
                                        phone_event=self.event['phone_event'],
                                        start_date_proposal=self.event['start_date_proposal']
                                        , end_date_proposal=self.event['end_date_proposal'],
                                        email_event=self.event['email_event']
                                        , beca_start=self.event['beca_start'], beca_end=self.event['beca_end'],
                                        max_inscription=self.event['max_inscription'],)

    def create_user(self):
        return User.objects.create_user(username=self.user['username'], email=self.user['email'],
                                        password=self.user['password'])

    def create_topic(self):
        return Topic.objects.create(name=self.topic['name'], color=self.topic['color'])

    def create_type_activity(self):
        return SpeechType.objects.create(name=self.speech_type)

    def create_room(self):
        return Room.objects.create(name=self.room['name'], spaces=self.room['spaces'], map=self.room['map'])

    def create_activity(self):
        event = self.create_event()
        user = self.create_user()
        topic = self.create_topic()
        type = self.create_type_activity()

        return Speech.objects.create(user=user, speaker_information=self.activity['speaker_information'],
                                     title=self.activity['title'], description=self.activity['description'],
                                     topic=topic, audience=self.activity['audience'],
                                     skill_level=self.activity['skill_level'], notes=self.activity['notes'],
                                     speech_type=type, presentacion=self.activity['presentation'],
                                     event=event)

    def create_speechSchedule(self):
        speech = self.create_activity()
        room = self.create_room()
        return SpeechSchedule.objects.create(start_time=self.speech_schedule['start_time'],
                                             end_time=self.speech_schedule['end_time'], speech=speech, room=room)



    def create_block_schedule(self):
        return BlockSchedule.objects.create(start_time=self.block_schedule['start_time'],
                                             end_time=self.block_schedule['end_time'],
                                             is_speech=self.block_schedule['is_speech'],
                                             text=self.block_schedule['text'], color=self.block_schedule['color'])


    def control_test(self):
        self.create_speechSchedule()
        self.create_block_schedule()


    def test_agenda_days_list(self):
        """
            With this test we are checking the basic flow when we go to agenda module from client side.
            1. first we send a request we the help of Cliente module to /agenda.
            2. we get a response as a result
            3. we check if response.context teh list of days that was create on get_context_data method
             view are equals to the list days on setUp function of the TestCase.

             output result = True
        """
        self.control_test()
        cliente = Client()
        response = cliente.get('/agenda')

        self.assertEqual(response.context['dayList'], self.days_list)

    def test_agenda_not_event(self):
        """
            here we are trying to visit agenda without an event created, and then we get the response and take the attr
            url from it and check if is redirect to the correct view.

            output result = True
        """
        cliente = Client()
        response = cliente.get('/agenda')

        self.assertEqual(response.url, 'sineventos/')


    def test_block_schedule(self):
        """
            This test help us to validate if we get as a result the expected length of the block schedule list getting
            when we go to specific day of the list days in the event.

            we have two block schedule on the day two
        """

        self.control_test()
        self.create_block_schedule()
        cliente = Client()
        response = cliente.get('/agenda?dia=2')
        self.assertEqual(len(response.context['object_list']), 2)
