import tempfile

from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory

# Create your tests here.
# Create Type

# CTy1
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from ecsl.models import EventECSL
from django.contrib.auth.models import User
from django.test import TestCase, Client
import datetime

from proposal.models import SpeechType, Topic, Speech

from proposal.forms import SpeechForm

from proposal.views import CreateType, CreateTopic, createUpdateview


class TestTopic(TestCase):

    def setUp(self):
        self.cliente = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='daniel',
                                             email='daniel@mail.com',
                                             password='daniel')
        self.event = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Panama',
                               description='description',
                               start_date=timezone.now() + timezone.timedelta(days=-1),
                               end_date=timezone.now() + timezone.timedelta(days=1),
                               current=True,
                               start_date_proposal=timezone.now() + timezone.timedelta(days=-1),
                               end_date_proposal=timezone.now() + timezone.timedelta(days=1)
                               )

        self.topic = Topic(name='Artificial Inteligence',
                           color='#cccccc',
                           event=self.event)

        self.speechType = SpeechType(name='Conversatory',
                                     time=60,
                                     event=self.event,
                                     is_special=False)
        self.speech = Speech(user=self.user,
                             speaker_information='AI expert',
                             title='Deep Learning',
                             description='Deep learning Algorithms',
                             topic=self.topic,
                             audience='everybody',
                             notes='Nope',
                             speech_type=self.speechType,
                             event=self.event,
                             is_scheduled=True)

        self.speech2 = Speech(user=self.user,
                             speaker_information='AI expert2',
                             title='Deep Learning2',
                             description='Deep learning Algorithms2',
                             topic=self.topic,
                             audience='everybody2',
                             notes='Nope2',
                             speech_type=self.speechType,
                             event=self.event,
                             is_scheduled=True)


 # CTo1:
    def test_Create_Topic(self):
        self.event.save()
        self.user.save()
        dataDic = { 'name': 'Test',
                    'color': '#cccccc',
                    'event': self.event.pk
                  }
        request = self.factory.post(reverse('proposal:create-topic'), dataDic)
        request.user = self.user
        view = CreateTopic()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(Topic.objects.last().name, 'Test')
        self.assertRedirects(response, reverse_lazy('list_charlas'), fetch_redirect_response=False)

    # CTo2:
    def test_Create_Topic_not_Logged(self):
        self.event.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'color': '#cccccc',
                   'event': self.event.pk
                   }
        request = self.factory.post(reverse('proposal:create-topic'), dataDic)
        view = CreateTopic()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(Topic.objects.last().name, 'Test')
        self.assertRedirects(response, reverse_lazy('list_charlas'), fetch_redirect_response=False)

    # CTo3:
    def test_Create_Topic_form_invalid(self):
        self.event.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'color': '#cccccc',
                   'event': self.event
                   }
        request = self.factory.post(reverse('proposal:create-topic'), dataDic)
        request.user = self.user
        view = CreateTopic()
        view.setup(request)
        response = view.dispatch(request)
        self.assertFalse(Topic.objects.last())
        self.assertRedirects(response, reverse_lazy('list_charlas'), fetch_redirect_response=False)

    # CTo1:
    def test_Create_Topic_two_events(self):
        self.event.save()
        self.user.save()
        event2= EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                               location='Nicaragua',
                               description='description2',
                               start_date=timezone.now() + timezone.timedelta(days=-1),
                               end_date=timezone.now() + timezone.timedelta(days=1),
                               current=True,
                               start_date_proposal=timezone.now() + timezone.timedelta(days=-1),
                               end_date_proposal=timezone.now() + timezone.timedelta(days=1)
                               )
        event2.save()
        dataDic = {'name': 'Test',
                   'color': '#cccccc',
                   'event': self.event.pk
                   }
        request = self.factory.post(reverse('proposal:create-topic'), dataDic)
        request.user = self.user
        view = CreateTopic()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(Topic.objects.filter(event=self.event.pk).last().name, 'Test')
        self.assertFalse(Topic.objects.filter(event=event2.pk).last())
        self.assertRedirects(response, reverse_lazy('list_charlas'), fetch_redirect_response=False)