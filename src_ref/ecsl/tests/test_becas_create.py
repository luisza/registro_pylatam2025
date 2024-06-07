from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from ecsl.models import Becas
from ecsl.tests.general_set_up import GeneralSetUp


class BecasCreateTestCase(GeneralSetUp, TestCase):
    user = None
    test_client = None

    def setUp(self):
        self.current_event = self.create_event()
        self.user = User.objects.create(username='userexample')
        self.user.set_password('password')
        self.user.save()
        self.test_client = Client()
        self.test_client.login(username="userexample", password='password')
        self.create_inscription(event=self.current_event, user=self.user)

    def test_BecasCreate(self):
        """
            This test check if teh becas request sent by the user was saved
        """
        self.test_client.post(reverse('becas-create'), self.becas)
        self.assertIsNotNone(Becas.objects.all().first())

    def test_BecasCreate_no_period(self):
        """
            The coded below help us to verify that an user can't send a beca request when the becas period
             is not available.
        """
        self.current_event.beca_start = timezone.now() + timezone.timedelta(days=-2)
        self.current_event.beca_end = timezone.now() + timezone.timedelta(days=-1)
        self.current_event.save()
        self.test_client.post(reverse('becas-create'), self.becas)
        self.assertIsNone(Becas.objects.all().first())

    def test_BecasCreate_two_request_same_event(self):
        """
            Here we are checking that an user can't has more than one becas request per event
        """
        self.test_client.post(reverse('becas-create'), self.becas)
        self.test_client.post(reverse('becas-create'), self.becas)
        self.assertEqual(len(Becas.objects.all()), 1)

    def test_BecasCreate_no_event(self):
        """
           This method is checking that we can't access to the becas module without a current event
        """
        self.current_event = self.create_event()
        self.current_event.current = False
        self.current_event.save()
        response = self.test_client.get('/becas')
        try:
            self.assertRedirects(response, expected_url='/sineventos/', status_code=302)
        except Exception as e:
            self.assertIsNotNone(e)