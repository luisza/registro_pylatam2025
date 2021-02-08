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


class TestViews(TestCase):

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

# Create Update View

    # CUV1
    def test_Create_Update_View(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        url = '/proposal/' + str(self.speech.pk) + '/update/'
        dataDic = {
                'speaker_information': 'personal info',
                'title': 'testSpeech',
                'description': 'test description',
                'topic': self.topic.pk,
                'audience': 'everybody',
                'skill_level':2,
                'notes': 'none',
                'speech_type': self.speechType.pk
                }
        request= self.factory.post(url, dataDic)
        request.user = self.user
        response= createUpdateview(request)
        self.assertEqual(response.url, reverse('proposal:speech-list'))
        self.assertEqual(Speech.objects.last().title,'testSpeech')

    # CUV2
    def test_Create_Update_View_No_authenticated(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        url = '/proposal/' + str(self.speech.pk) + '/update/'
        response = self.cliente.get(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(messages[0],
                         'Lo sentimos ! Para poder enviar una propuesta de charla tiene que estar registrado como usuario en nuestro sistema.')

    #CUV3
    def test_Create_Update_View_form_invalid_speech(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        url = '/proposal/' + str(self.speech.pk) + '/update/'
        dataDic = {
                'speaker_information': 'personal info',
                'title': 'testSpeech',
                'description': 'test description',
                'topic': self.topic,
                'audience': 'everybody',
                'skill_level':'errorThisWasAnInt',
                'notes': 'none',
                'speech_type': self.speechType.pk
                }
        request= self.factory.post(url, dataDic)
        request.user = self.user
        response= createUpdateview(request)
        self.assertEqual(response.url, reverse('proposal:speech-list'))
        self.assertFalse(Speech.objects.filter(title='testSpeech').last())

    # CUV4
    def test_Create_Update_View_no_event_or_proposal(self):
        self.event.start_date_proposal= timezone.now() - timezone.timedelta(days=5)
        self.event.end_date_proposal= timezone.now() - timezone.timedelta(days=5)
        self.event.save()
        self.user.save()
        self.cliente.login(username='daniel', password='daniel')
        url = reverse('proposal:create')
        response = self.cliente.get(url)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(messages[0],
                         'Lo sentimos! No estamos en periodo de envíos de propuestas para charlas')

    # CUV5
    def test_Create_Update_View_no_speech(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        url = reverse('proposal:create')
        dataDic = {
            'speaker_information': 'personal info',
            'title': 'testSpeech',
            'description': 'test description',
            'topic': self.topic.pk,
            'audience': 'everybody',
            'skill_level': 2,
            'notes': 'none',
            'speech_type': self.speechType.pk
        }
        request = self.factory.post(url, dataDic)
        request.user = self.user
        response = createUpdateview(request)
        self.assertEqual(response.url, reverse('proposal:speech-list'))
        self.assertEqual(Speech.objects.last().title, 'testSpeech')

    # CUV6
    def test_Create_Update_View_form_invalid_no_speech(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        url = reverse('proposal:create')
        dataDic = {
            'speaker_information': 'personal info',
            'title': 'testSpeech',
            'description': 'test description',
            'topic': self.topic.pk,
            'audience': 'everybody',
            'skill_level': 'errorThisWasAnInt',
            'notes': 'none',
            'speech_type': self.speechType.pk
        }
        request = self.factory.post(url, dataDic)
        request.user = self.user
        response = createUpdateview(request)
        self.assertEqual(response.url, reverse('proposal:speech-list'))
        self.assertFalse(Speech.objects.last())


    # CUV7
    def test_Create_Update_View_GET(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        self.cliente.login(username='daniel', password='daniel')
        url = '/proposal/' + str(self.speech.pk) + '/update/'
        response = self.cliente.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proposal/speech_form.html')

    # CUV8
    def test_Create_Update_View_other_user(self):
        self.event.save()
        self.user.save()
        self.speechType.save()
        self.topic.save()
        self.speech.save()
        newuser = User.objects.create_user( username='other',
                                            email='other@mail.com',
                                            password='other')
        url = '/proposal/' + str(self.speech.pk) + '/update/'
        dataDic = {
                'speaker_information': 'personal info',
                'title': 'testSpeech',
                'description': 'test description',
                'topic': self.topic.pk,
                'audience': 'everybody',
                'skill_level':2,
                'notes': 'none',
                'speech_type': self.speechType.pk
                }
        request= self.factory.post(url, dataDic)
        request.user = newuser
        response= createUpdateview(request)
        self.assertEqual(response.url, reverse('proposal:speech-list'))
        self.assertFalse(Speech.objects.last())