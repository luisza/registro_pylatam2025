from django.test import TestCase, Client
from django.urls import reverse
from .shared_methods import create_user, create_eventECSL, create_payment, create_package, \
    create_payment_option, create_inscription, create_block_schedule, create_room, create_topic, create_type, \
    create_speech, create_speech_schedule
from ecsl.models import Inscription, Payment, EventECSL

USER_NAME = 'test'
USER_EMAIL = 'test@mail.com'
PASSWORD = 'testtest'


class MyAgendaTest(TestCase):
    """
        This view displays all the speeches in which the user is registered on the current day.
        Each speech has its start time, title (which is a link to the speech detail),
        expositor's name, room, and an option to deregister from the selected speech.
    """

    def setUp(self):
        self.client = Client()
        self.user = create_user(USER_NAME, USER_EMAIL, PASSWORD)
        self.block_schedule = create_block_schedule()
        self.event = create_eventECSL()
        self.payment_option = create_payment_option(self.event)
        self.package = create_package(self.event)
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)
        self.inscription = create_inscription(self.user, self.event)
        self.room = create_room(self.event)
        self.topic = create_topic(self.event)
        self.type = create_type(self.event)
        self.speech = create_speech(self.user, self.event, self.topic, self.type)
        self.speech_schedule = create_speech_schedule(self.speech, self.room)

    def test_my_agenda(self):
        """ happy path
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('mi_agenda'))
        self.assertEqual(response.status_code, 200)

    def test_my_agenda_no_payment(self):
        """

        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        Payment.objects.filter(user=self.user).update(confirmado=False)

        response = self.client.get(reverse('mi_agenda'))
        self.assertRedirects(response, reverse('index'))
        Payment.objects.filter(user=self.user).update(confirmado=True)

    def test_my_agenda_no_inscription(self):
        """

        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        Inscription.objects.filter(user=self.user).delete()

        response = self.client.get(reverse('mi_agenda'))
        self.assertRedirects(response, reverse('index'))
        self.inscription = create_inscription(self.user, self.event)

    def test_my_agenda_not_logged_in_user(self):
        """

        """
        response = self.client.get(reverse('mi_agenda'))
        self.assertRedirects(response, '/accounts/login/?next=/miagenda')

    def test_no_active_event(self):
        """
            When there is no an active evente, the user should be redirected to the no event page.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        EventECSL.objects.filter(current=True).update(current=False)
        response = self.client.get(reverse('mi_agenda'))
        self.assertRedirects(response, '/sineventos/')
        EventECSL.objects.filter(current=False).update(current=True)
