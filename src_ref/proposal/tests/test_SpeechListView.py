from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus
from ecsl.tests.shared_methods import create_user, create_eventECSL, not_logged_in_user, create_type, create_topic, \
    create_speech
from datetime import datetime, timedelta
from ecsl.models import EventECSL
from proposal.models import Speech, SpeechType

USER_NAME = 'test3'
USER_EMAIL = 'test3@mail.com'
PASSWORD = 'testtest3'


class SpeechListViewTest(TestCase):
    """
        The page shows all the speech proposals made by the user. If the period for receiving a proposal is active, an
        Add button is displayed in order to create a new speech proposal. If the period to make a speech proposal is no
        longer valid and the user submitted at least one before the finalization period, the user can still see its
        proposals, otherwise, the access to this page should not be allowed.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.topic = create_topic(self.event)
        self.type = create_type(self.event)
        self.speech = create_speech(self.user, self.event, self.topic, self.type)

    def test_speech_list_view(self):
        """
            The user’s speech proposals are displayed in list way. Each proposal has two buttons, one for editing and
            other for deleting. As the receiving period is open, add proposal button is shown.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:speech-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>')
        self.assertContains(response, '<span class="glyphicon glyphicon-edit" aria-hidden="true"></span>')
        self.assertContains(response, '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>')
        self.assertContains(response, self.speech)

    def test_speech_list_view_not_logged_in_user(self):
        """
            When accessing via URL, the user should be redirected to the index page.
        """
        target = '/proposal/'
        redirect_to = '/'
        not_logged_in_user(self, target, redirect_to)

    def test_speech_list_view_receiving_period_ended_with_speeches(self):
        """
            The page is displayed with the user’s speech proposal but the Add button is not shown.
        """
        self.event.end_date_proposal = datetime.today().date() - timedelta(days=2)
        self.event.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:speech-list'))
        self.assertNotContains(response, '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>')

        self.event.end_date_proposal = datetime.today().date()
        self.event.save()

    def test_speech_list_view_receiving_period_ended_with_no_speeches(self):
        """
            The page is displayed with the user’s speech proposal but the Add button is not shown.
        """
        self.event.end_date_proposal = datetime.today().date() - timedelta(days=2)
        self.speech.delete()
        self.event.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:speech-list'))
        self.assertRedirects(response, reverse('index'))

        self.event.end_date_proposal = datetime.today().date()
        self.event.save()
        self.speech = create_speech(self.user, self.event, self.topic, self.type)

    def test_speech_list_view_more_than_ten_speeches(self):
        """
            When a user has many speech proposals, the page should only be displaying a maximum of ten proposals per
            page.
        """
        for i in range(11):
            self.speech = create_speech(self.user, self.event, self.topic, self.type)

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:speech-list'))
        self.assertContains(response, '<ul class="pager">')

        Speech.objects.filter(user=self.user).delete()
        self.speech = create_speech(self.user, self.event, self.topic, self.type)

    def test_speech_list_view_no_active_event(self):
        """
            As an active event has not been established, the user should  be redirected to the index page.
        """
        EventECSL.objects.filter(pk=self.event.pk).update(current=False)
        self.client.login(username=USER_NAME, password=PASSWORD)

        response = self.client.get(reverse('proposal:speech-list'))
        self.assertEqual(response.status_code, 302)

        EventECSL.objects.filter(pk=self.event.pk).update(current=True)

    def test_speech_list_view_user_has_no_speeches(self):
        """
            If the user has no speech proposals, only the add proposal button must be displayed
        """
        self.speech.delete()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:speech-list'))

        self.assertContains(response, '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>')
        self.assertNotContains(response, '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>')
        self.assertNotContains(response, '<span class="glyphicon glyphicon-edit" aria-hidden="true"></span>')
