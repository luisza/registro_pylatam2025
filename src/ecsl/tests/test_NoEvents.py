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

class TestNoEvent(TestCase):

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

    # NoEv1:
    def test_index_with_event(self):
        self.event.save()
        response = self.cliente.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    # NoEv2:
    def test_index_no_event(self):
        request = self.cliente.get(reverse('index'))
        response = Index.as_view()(request)

        self.assertRedirects(response, '/sineventos/', status_code=302, target_status_code=200,
                             fetch_redirect_response=False)

