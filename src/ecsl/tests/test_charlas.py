import json
from unittest import skip
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone
from proposal.models import Room
from .general_set_up import GeneralSetUp

class CharlasTestCase(TestCase, GeneralSetUp):
    days_list = None
    current_event = None
    initial_room = None
    test_client = None

    def setUp(self):
        """
            Lista of days form start_date to end_date in an event
        """
        self.initial_room = self.create_room()
        self.days_list = [(timezone.now() + timezone.timedelta(days=-1)).date(), timezone.now().date(),
                          (timezone.now() + timezone.timedelta(days=1)).date(),
                          (timezone.now() + timezone.timedelta(days=2)).date(),
                          (timezone.now() + timezone.timedelta(days=3)).date(),
                          (timezone.now() + timezone.timedelta(days=4)).date()]
        self.test_client = Client()

    def test_agenda_days_list(self):
        """
            With this test we are checking the basic flow when we go to agenda module from client side.
            1. first we send a request we the help of Cliente module to /agenda.
            2. we get a response as a result
            3. we check if response.context the list of days that was create on get_context_data method
             view are equals to the list days on setUp function of the TestCase.

             output result = True
        """
        self.control_test()
        response = self.test_client.get('/agenda')

        self.assertEqual(response.context['dayList'], self.days_list)

    def test_agenda_not_event(self):
        """
            here we are trying to visit agenda without an event created, and then we get the response and take the attr
            url from it and check if is redirect to the correct view.

            output result = True
        """
        response = self.test_client.get('/agenda')

        self.assertRedirects(response, '/sineventos/', status_code=302)

    def test_block_schedule_specific_day(self):
        """
            This test help us to validate if we get as a result the expected length of the block schedule list getting
            when we go to specific day of the list days in the event.

            we have two block schedule on the day two
        """

        self.control_test()
        self.create_block_schedule()
        response = self.test_client.get('/agenda?dia=2')
        self.assertEqual(len(response.context['object_list']), 2)

    def test_block_schedule_specific_room(self):
        """
            This test help us to validate if we get as a result the expected length of the block schedule list getting
            when we go to specific day and room.

            we have two block schedule on the day two and room Two
        """
        self.current_event = self.create_event()
        self.create_room()
        self.room['name'] = 'myroom 2'
        room = self.create_room()
        self.create_speechSchedule(room=room,
                                   speech=self.create_activity(scheduled=True))
        self.activity['title'] = "testing 2"

        self.create_speechSchedule(room=room,
                                   speech=self.create_activity(user=User.objects.all().first(), scheduled=True))
        self.create_block_schedule(room=room)
        response = self.test_client.get('/agenda?dia=2&sala=2')
        self.assertEqual(len((json.loads(response.context['stored_activities_dic']))), 2)

    @skip("room conflict, must to be fixed")
    def test_agenda_without_room(self):
        """
            This test help us to check the behavior of the charlas view , when the event does not have a room saved,
            the view need to redirect to the index page.
        """
        Room.objects.all().delete()
        self.create_event()
        response = self.test_client.get('/agenda')
        self.assertRedirects(response, '', status_code=200)

    def test_finding_an_invalid_day(self):
        """
            the code below allow us to know the view behavior when an user adds invalid valued into the url
            trying to get an specific day through it.
        """
        self.control_test()
        response = self.test_client.get('/agenda? dia=520')
        self.assertTemplateUsed(response, 'proposal/blockschedule_list.html')