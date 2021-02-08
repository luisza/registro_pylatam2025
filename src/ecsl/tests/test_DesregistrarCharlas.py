from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse
from .shared_methods import create_user, create_eventECSL, create_payment, create_package, \
    create_payment_option, create_inscription, create_block_schedule, create_room, create_topic, create_type, \
    create_speech, create_speech_schedule
from datetime import datetime, date
from proposal.models import Register_Speech, SpeechSchedule, Speech

start_time = datetime(2021, 1, 13, hour=12, minute=0, second=0)
end_time = datetime(2021, 1, 13, hour=13, minute=30, second=0)
start_date = date(2021, 1, 12)
end_date = date(2021, 1, 14)
beca_start = date(2021, 1, 12)
beca_end = date(2021, 1, 12)
proposal_start = date(2021, 1, 12)
proposal_end = date(2021, 1, 12)

USER_NAME = 'test'
USER_EMAIL = 'test@mail.com'
PASSWORD = 'testtest'


def register_user_speech(speech_schedule, user):
    return Register_Speech.objects.create(speech=speech_schedule, user=user)


class DesregistrarCharlaTest(TestCase):
    """
        When an user registered into a speech and he/she no longer wants to be a participant,
        the "Deregister" button makes this possible. This action can be reached through the buttons
        in "My Agenda" or speech detail pages or via URL.
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
        self.register_speech = register_user_speech(self.speech_schedule, self.user)

    def test_desregistrar_charla(self):
        """
        When the "Deregister" button is hit, the user gets redirected to the Agenda page. The associate
        record is deleted from the database and there should be one more space available in the room.
        """
        temp_speech = create_speech(self.user, self.event, self.topic, self.type)
        temp_speech_schedule = create_speech_schedule(temp_speech, self.room)
        temp_register_speech = register_user_speech(temp_speech_schedule, self.user)

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('desregistrar_charla', kwargs={'pk': temp_register_speech.pk}) +
                                   "?dia=%d&fecha=%s" % (2, temp_speech_schedule.start_time))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        Register_Speech.objects.all().delete()
        SpeechSchedule.objects.filter(pk=temp_speech_schedule.pk).delete()
        Speech.objects.filter(pk=temp_speech.pk).delete()

    def test_desregistrar_charla_user_not_logged(self):
        response = self.client.get(reverse('desregistrar_charla', kwargs={'pk': self.register_speech.pk}))
        self.assertRedirects(response, '/accounts/login/?next=/charla/desregistrar/%d' % (self.register_speech.pk))

    def test_desregistrar_charla_wrong_day(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('desregistrar_charla', kwargs={'pk': self.register_speech.pk}) +
                                   "?dia=%d&fecha=%s" % (7, self.speech_schedule.start_time))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.register_speech = register_user_speech(self.speech_schedule, self.user)

    def test_desregistar_charla_deregister_user_not_registered(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('desregistrar_charla', kwargs={'pk': (self.register_speech.pk + 200)}) +
                                   "?dia=%d&fecha=%s" % (2, self.speech_schedule.start_time))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
