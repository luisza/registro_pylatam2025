import random

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now
import random
from ecsl.models import EventECSL
from proposal.models import Room, SpeechType, Topic, Speech


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--stmont', type=int, default=3, help='Meses posteriores a la fecha')
        parser.add_argument('--duration', type=int, default=3, help='Duración del evento en días')
        parser.add_argument('--rooms', type=int, default=3, help='Número de salas')
        parser.add_argument('--speechusers', type=int, default=6, help='Número de charlistas')
        parser.add_argument('--nocurrent', default=True, action='store_false')
        parser.add_argument('--clean', type=bool, default=False, help='Limpiar la base de datos actual')

    def create_random_color(self):
        color = "%06x" % random.randint(0, 0xFFFFFF)
        return "#"+color

    def create_topics(self, event):
        Topic.objects.create(name='Linux Básico',
            color=self.create_random_color(), event=event)
        Topic.objects.create(name='Linux Técnico',
            color=self.create_random_color(), event=event)
        Topic.objects.create(name='Informática y sociedad',
            color=self.create_random_color(), event=event)
        Topic.objects.create(name='Mujeres en comunidades de Software Libre',
            color=self.create_random_color(), event=event)

    def create_speechtype(self, event):
        SpeechType.objects.create(
            name='Almuerzo',
            time = 60,
            event = event,
            is_special = True
        )
        SpeechType.objects.create(
            name='Receso merienda mañana',
            time = 15,
            event = event,
            is_special = True
        )
        SpeechType.objects.create(
            name='Receso merienda tarde',
            time = 15,
            event = event,
            is_special = True
        )

        SpeechType.objects.create(
            name='Charla',  time = 40,
            event = event,  is_special = False
        )
        SpeechType.objects.create(
            name='Micro charla',  time = 20,
            event = event,  is_special = False
        )
        SpeechType.objects.create(
            name='Taller',  time=180,
            event=event,  is_special=False
        )
        SpeechType.objects.create(
            name='Conversatorio',  time=120,
            event=event,  is_special=False
        )

    def create_room(self, options, event):
        for x in range(options['rooms']):
            Room.objects.create(
                name='room %d / %d'%(event.pk, x),
                spaces = random.randint(0, 50),
                event = event
            )

    def create_event(self, options):
        event = EventECSL.objects.create(
            start_date=now()+relativedelta(months=options['stmont']),
            end_date=now()+relativedelta(months=options['stmont'], days=options['duration']),
            description='Test event',
            current=options['nocurrent'],
            organizer1='Juan',
            organizer2='Diego',
            phone_event='8888888',
            start_date_proposal=now()+relativedelta(months=options['stmont'], days=-10),
            end_date_proposal=now()+relativedelta(months=options['stmont'], days=-1),
            beca_start=now()+relativedelta(months=options['stmont'], days=-10),
            beca_end=now()+relativedelta(months=options['stmont'], days=-1),
            max_inscription=250
        )
        return event

    def speech_creator(self, options, event):
        speeaches = []
        for number in range(options['speechusers']):

            user=User.objects.create_user('user%d_%d'%(event.pk, number),
                                          'user%d_%d@mailinator.com'%(event.pk, number),
                                          'admin12345')
            instance=Speech(user=user, speaker_information="speaker {}".format(number),
                                         title="Speech {}".format(number), description="description {}".format(number),
                                         topic=Topic.objects.filter(event=event).order_by("?").first(), audience="audience {}".format(number),
                                         skill_level=1, notes="notes {}".format(number),
                                         speech_type=SpeechType.objects.filter(is_special=False, event=event).
                                         order_by("?").first(), presentacion="presentacion {}".format(number),
                                         event=event)
            instance.speech_time_asked = instance.speech_type.time
            speeaches.append(instance)

        Speech.objects.bulk_create(speeaches)
        return speeaches

    def clean_db(self):
        """ Cleans db stored data """
        # All models class depends on cascade with Events
        EventECSL.objects.all().delete()

    def handle(self, *args, **options):
        try:
            from dateutil.relativedelta import relativedelta
        except:
            print("Please install  python-dateutil")
            exit(1)
        event = self.create_event(options)
        self.create_room(options, event)
        self.create_speechtype(event)
        self.create_topics(event)
        self.speech_creator(options, event)

        # Handles clean db
        if options['clean']:
            self.clean_db()