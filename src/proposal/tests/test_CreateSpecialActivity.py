from unittest import skip

from django.contrib.auth.models import Permission, User
from django.test import TestCase, Client
from django.urls import reverse
from ecsl.tests.shared_methods import create_user, create_eventECSL, not_logged_in_user, create_type, create_topic, \
    create_speech
from http import HTTPStatus
from proposal.models import Speech, SpeechType

USER_NAME = 'test3'
USER_EMAIL = 'test3@mail.com'
PASSWORD = 'testtest3'


class CreateSpecialActivityTest(TestCase):
    """
        Form is displayed in order to create a new Special Activity.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.event = create_eventECSL()
        self.type = SpeechType.objects.create(name="Test Special Type", time=20, event=self.event, is_special=True)

    def test_create_special_activity(self):
        """
            A form to create a special activity is displayed. It has three fields: name, type and message. After
            submitting the user must be redirected to de list_charlas page.
        """
        self.user.user_permissions.add(Permission.objects.get(codename='add_specialactivity'))
        self.user.save()

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.post(reverse('proposal:create-special'), data={
            'name': 'Special Activity Test',
            'type': self.type.pk,
            'message': 'Creating special activity'
        })

        self.assertEqual(response.status_code, 302)

