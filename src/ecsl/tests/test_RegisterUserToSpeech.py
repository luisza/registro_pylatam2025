from django.test import TestCase, Client
from datetime import datetime, date
from django.urls import reverse
from .shared_methods import create_user, create_eventECSL, not_logged_in_user, create_payment, create_package, \
    create_payment_option, create_inscription, create_room, create_topic, create_block_schedule, create_type, \
    create_speech, create_speech_schedule

from proposal.models import BlockSchedule, Room, Speech, SpeechSchedule, Register_Speech, SpecialActivity, Topic, \
    SpeechType
from ecsl.models import EventECSL, Inscription, Package, Payment, PaymentOption

start_time = datetime(2021, 1, 13, hour=12, minute=0, second=0)
end_time = datetime(2021, 1, 13, hour=13, minute=30, second=0)
start_date = date(2021, 1, 12)
end_date = datetime.today().date()
beca_start = date(2021, 1, 12)
beca_end = datetime.today().date()
proposal_start = date(2021, 1, 12)
beca_end = datetime.today().date()

USER_NAME = 'test'
USER_EMAIL = 'test@mail.com'
PASSWORD = 'testtest'


class RegisterUserToSpeechTest(TestCase):
    """
        In the speech details, the user hits the "Register" button. This action must verify that
        speech takes place on the day the user has requested, thus is a valid day; the user must be
        registered in the event with the payment done, the room where the speech is held must have
        enough space and there can be no schedule clash.
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

    def test_register_user_to_speech(self):
        """
            Once the "Register" button is hit, the user is taken as part of the activity's participants
            and the user is redirected to the Agenda page so he/can get registered into other activities.
            The room's available space must decrease one unit.
        """
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))

        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)
        Register_Speech.objects.filter(user=self.user).delete()

    def test_register_user_to_speech_user_not_logged(self):
        """
            This page should not be allowed for accessing to not logged in users. They should be redirected to the login
            page.
        """
        target = '/charla/registro/' + str(self.speech.pk)
        redirect_to = '/accounts/login/?next=' + target
        not_logged_in_user(self, target, redirect_to)

    def test_register_user_to_speech_no_inscription(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        Inscription.objects.filter(user=self.user).delete()
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)
        self.inscription = create_inscription(self.user, self.event)

    def test_register_user_to_speech_no_payment_confirmed(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        Payment.objects.filter(user=self.user).update(confirmado=False)

        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)
        Payment.objects.filter(user=self.user).update(confirmado=True)

    def test_register_user_to_speech_wrong_day(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)
        Register_Speech.objects.filter(user=self.user).delete()

    def test_register_user_to_speech_wrong_speech_pk(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk + 1}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)

    def test_register_user_to_speech_wrong_datetime(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': (self.speech.pk)}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day + 2,
                                       start_time.hour + 6, start_time.minute, start_time.second))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)

    def test_register_user_to_speech_no_payment_done(self):
        self.client.login(username=USER_NAME, password=PASSWORD)
        Payment.objects.filter(user=self.user).delete()

        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))
        self.assertRedirects(response, reverse('index'))
        Payment.objects.filter(user=self.user).update(confirmado=True)
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)
        self.payment = create_payment(self.user, self.payment_option, self.event, self.package)

    def test_register_user_to_speech_no_room_space(self):
        self.room.spaces = 0
        self.room.save()
        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))
        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 0)

        self.room.spaces = 2
        self.room.save()

    def test_register_user_to_speech_schedule_clash(self):
        temp_speech = create_speech(self.user, self.event, self.topic, self.type)
        temp_speech_schedule = SpeechSchedule.objects.create(start_time=start_time,
                                                             end_time=end_time,
                                                             speech=temp_speech,
                                                             special=None,
                                                             room=self.room)
        temp_register_speech = Register_Speech.objects.create(speech=temp_speech_schedule, user=self.user)
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))

        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)

        temp_register_speech.delete()
        temp_speech_schedule.delete()
        temp_speech.delete()

    def test_register_user_to_speech_register_same_event(self):
        Register_Speech.objects.create(speech=self.speech_schedule, user=self.user)
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)

        self.client.login(username=USER_NAME, password=PASSWORD)
        response = self.client.get(reverse('registra_charla', kwargs={'pk': self.speech.pk}) +
                                   "?dia=%d&year=%d&month=%d&day=%d&hour=%d&minute=%d&second=%d" % (
                                       2, start_time.year, start_time.month, start_time.day,
                                       start_time.hour, start_time.minute, start_time.second))

        self.assertRedirects(response, reverse('list_charlas') + "?dia=%d" % (1,))
        self.assertEqual(Register_Speech.objects.filter(user=self.user).count(), 1)
        Register_Speech.objects.all().delete()
