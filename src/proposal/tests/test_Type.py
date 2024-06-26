import tempfile
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from ecsl.models import EventECSL
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from proposal.models import SpeechType, Topic, Speech
from proposal.types import CreateType

# Create your tests here.
# Create Type

# CTy1



class TestType(TestCase):

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

    # Create Type

    # CTy1:
    def test_Create_Type(self):
        self.event.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'time': 60,
                   'event': self.event.pk,
                   'is_special': True}
        self.user.user_permissions.add(Permission.objects.get(codename='add_speechtype'))
        self.user.save()
        request = self.factory.post(reverse('proposal:create-type'), dataDic)
        request.user = self.user
        view = CreateType()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(SpeechType.objects.last().name, 'Test')
        self.assertRedirects(response, reverse_lazy('edit_charlas'), fetch_redirect_response=False)

    # CTy2:
    def test_Create_Type_not_Logged(self):
        self.event.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'time': 60,
                   'event': self.event.pk,
                   'is_special': True}
        self.user.user_permissions.add(Permission.objects.get(codename='add_speechtype'))
        self.user.save()
        request = self.factory.post(reverse('proposal:create-type'), dataDic)
        request.user = self.user
        view = CreateType()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(SpeechType.objects.last().name, 'Test')
        self.assertRedirects(response, reverse_lazy('edit_charlas'), fetch_redirect_response=False)

    # CTy3:
    def test_Create_Type_Invalid_Form(self):
        self.event.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'time': 60,
                   'event': self.event,
                   'is_special': True}
        self.user.user_permissions.add(Permission.objects.get(codename='add_speechtype'))
        self.user.save()
        request = self.factory.post(reverse('proposal:create-type'), dataDic)
        view = CreateType()
        view.setup(request)
        response = view.dispatch(request)
        self.assertFalse(SpeechType.objects.last())
        self.assertRedirects(response, reverse_lazy('edit_charlas'), fetch_redirect_response=False)

    # CTy4:
    def test_Create_Type_Two_Events(self):
        self.event.save()
        event2 = EventECSL(logo=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                           location='Nicaragua',
                           description='description2',
                           start_date=timezone.now() + timezone.timedelta(days=-1),
                           end_date=timezone.now() + timezone.timedelta(days=1),
                           current=True,
                           start_date_proposal=timezone.now() + timezone.timedelta(days=-1),
                           end_date_proposal=timezone.now() + timezone.timedelta(days=1)
                           )
        event2.save()
        self.user.save()
        dataDic = {'name': 'Test',
                   'time': 60,
                   'event': self.event.pk,
                   'is_special': True}
        self.user.user_permissions.add(Permission.objects.get(codename='add_speechtype'))
        self.user.save()
        request = self.factory.post(reverse('proposal:create-type'), dataDic)
        view = CreateType()
        view.setup(request)
        response = view.dispatch(request)
        self.assertEqual(SpeechType.objects.filter(event=self.event.pk).last().name, 'Test')
        self.assertFalse(SpeechType.objects.filter(event=event2.pk))
        self.assertRedirects(response, reverse_lazy('edit_charlas'), fetch_redirect_response=False)