from django.test import TestCase, Client
from django.urls import reverse
from ecsl.tests.shared_methods import create_user, create_eventECSL, not_logged_in_user, create_type, create_topic, \
    create_speech
from proposal.models import Speech, SpeechType


USER_NAME = 'test3'
USER_EMAIL = 'test3@mail.com'
PASSWORD = 'testtest3'


class DeleteViewTest(TestCase):
    """
        It deletes the selected speech proposal from the database.
    """
    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.topic = create_topic(self.event)
        self.type = create_type(self.event)
        self.speech = create_speech(self.user, self.event, self.topic, self.type)

    def test_delete_view(self):
        """
            The speech is deleted after calling this view.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('proposal:delete', kwargs={'speech_id': self.speech.pk}))
        self.assertRedirects(response, reverse('proposal:speech-list'))
        self.assertEqual(Speech.objects.filter(pk=self.speech.pk).count(), 0)
        self.speech = create_speech(self.user, self.event, self.topic, self.type)

    def test_delete_view_not_logged_in_user(self):
        """
            When accessing via URL, user should be redirected to the index page.
        """

        target = '/proposal/' + str(self.speech.pk) + '/delete/'
        redirect_to = '/'
        not_logged_in_user(self, target, redirect_to)

    def test_delete_view_get_method(self):
        """
            As the view only deletes if the request is a POST, accessing from the URL does not delete any activity,
            it only redirects to the proposal page.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('proposal:delete', kwargs={'speech_id': self.speech.pk}))
        self.assertRedirects(response, reverse('proposal:speech-list'))

        self.assertEqual(Speech.objects.filter(pk=self.speech.pk).count(), 1)
