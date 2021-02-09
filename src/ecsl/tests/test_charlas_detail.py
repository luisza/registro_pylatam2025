import json
from unittest import skip

import html5lib
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone
from ecsl.models import Payment, EventECSL
from ecsl.tests.general_set_up import GeneralSetUp
from proposal.models import Speech


class CharlasDetailTestCase(GeneralSetUp, TestCase):
    test_client = None

    def setUp(self):
        self.test_client = Client()

    @skip("Translation issues")
    def test_speech_detail_current_event_false(self):
        """
          The following code helps us to check that we cannot see any detail speech when the system does not have
          stored events or when the events are disabled.

          we set all needed objects on the data base, then we update current field on event, and finally we request
          to the first speech on the data base

          we are expecting that the system does not show us the detail of the requested speech detail.
        """
        self.control_test()
        speech = Speech.objects.first()
        event = EventECSL.objects.first()
        event.current = False
        event.save()
        response = self.test_client.get('/charla/%s' % speech.id)
        self.assertEqual('No Actividad found matching the query', response.context['exception'])

    def test_checking_button_to_log_in(self):
        """
           These test allow us to check if the button which redirect to the log in page when the user is not register
           in the system
        """
        self.current_event = self.create_event()
        room = self.create_room()
        self.create_speechSchedule(room=room,
                                   speech=self.create_activity(user=User.objects.all().first(), scheduled=True))
        self.create_block_schedule(room=room)
        response = self.test_client.get('/agenda?dia=2&sala=1')
        id = json.loads(response.context['stored_activities_dic'])['1-{}'.format(Speech.objects.all().first().id)]
        detail_response = self.test_client.get('/charla/{}'.format(id['activity_pk']))
        parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
        document = parser.parse(detail_response.content.decode('utf-8'))
        url = None
        for tag in document.getElementsByTagName("a"):
            if tag.getAttribute('href') == '/accounts/login/?next=/agenda':
                url = tag.getAttribute('href')
        self.assertEqual(url, '/accounts/login/?next=/agenda')

    def test_checking_button_register_in_activity(self):
        """
           These test allow us to check if the button which register an user into activity is displayed if the user
           is logged and has been paid the inscription.
        """
        self.current_event = self.create_event()
        room = self.create_room()
        user = User.objects.create(username='userexample')
        user.set_password('password')
        user.save()
        self.create_speechSchedule(room=room,
                                   speech=self.create_activity(user=user, scheduled=True))
        self.create_block_schedule(room=room)
        self.test_client.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=user)
        self.create_payment(user=user, event=self.current_event, package=self.create_package(event=self.current_event),
                            option=self.create_payment_option(event=self.current_event))
        pago = Payment.objects.first()
        pago.confirmado = True
        pago.save()
        response = self.test_client.get('/agenda?dia=2&sala=1')
        id = json.loads(response.context['stored_activities_dic'])['1-{}'.format(Speech.objects.all().first().id)]
        detail_response = self.test_client.get('/charla/{}'.format(id['activity_pk']))
        parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
        document = parser.parse(detail_response.content.decode('utf-8'))
        url = None
        for tag in document.getElementsByTagName("a"):
            if tag.getAttribute(
                    'href') == '/charla/registro/{}?dia={}&year={}&month={}&day={}&hour={}&minute={}&second={}'.format(
                id['activity_pk'], 1, timezone.now().date().year, timezone.now().date().month,
                timezone.now().date().day, 0, 0, 0):
                url = tag.getAttribute('href')
        self.assertEqual(url, '/charla/registro/{}?dia={}&year={}&month={}&day={}&hour={}&minute={}&second={}'.format(
            id['activity_pk'], 1, timezone.now().date().year, timezone.now().date().month,
            timezone.now().date().day, 0, 0, 0))