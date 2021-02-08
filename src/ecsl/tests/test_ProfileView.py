from ecsl import views
from proposal.models import BlockSchedule, Speech, Topic, SpeechType, Room, SpeechSchedule
import datetime
from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ecsl.models import EventECSL, Inscription, Payment, PaymentOption, Package, Becas
from ecsl.views import Index, CustomContactFormCaptcha, contact

import tempfile
from django.test import TestCase, Client, RequestFactory, override_settings

class TestProfile(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='daniel',
                                             email='daniel@mail.com',
                                             password='daniel')
        self.event = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Panama',
                               description='description',
                               start_date=datetime.datetime(2021, 1, 15),
                               end_date=datetime.datetime(2022, 1, 15),
                               current=True,
                               start_date_proposal=datetime.datetime(2021, 1, 15),
                               end_date_proposal=datetime.datetime(2022, 1, 15))

        self.inscription = Inscription(user=self.user,
                                       status=2,
                                       gender='Masculino',
                                       nationality='Costa Rica',
                                       identification='123456789',
                                       direccion_en_su_pais='San Jose',
                                       born_date=datetime.datetime(1997, 8, 14),
                                       institution='Solvo',
                                       event=self.event)

 # Profile View

    # Pfv1
    def test_profile_view_user_inscribed(self):
        self.event.save()
        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        self.inscription.save()
        response = self.cliente.get(reverse('profile'))
        url = '/register/profile/update/' + str(self.inscription.pk)
        self.assertRedirects(response, url, status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    # Pfv2
    def test_profile_view_user_not_inscribed(self):
        self.event.save()
        self.cliente.login(username='daniel', password='daniel')
        response = self.cliente.get(reverse('profile'))
        url = reverse('create_profile')
        self.assertRedirects(response, url, status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

    # Pfv3
    def test_profile_view_user_not_logged(self):
        self.event.save()
        response = self.cliente.get(reverse('profile'))
        url = '/accounts/login/?next=' + reverse('profile')
        self.assertRedirects(response, url)