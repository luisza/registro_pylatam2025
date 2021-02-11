from django.core.management.base import BaseCommand
from proposal.models import Room, Speech, SpeechType, Topic
from ecsl.models import EventECSL
from django.contrib.auth.models import User

class Command(BaseCommand):

    def set_asked_time(self, speeches):
        for speech in speeches:
            speech.speech_time_asked = speech.speech_type.time
        return speeches


    def speech_creator(self):

        speeaches = [Speech(user=User.objects.first(), speaker_information="speaker {}".format(number),
                                         title="Speech {}".format(number), description="description {}".format(number),
                                         topic=Topic.objects.order_by("?").first(), audience="audience {}".format(number),
                                         skill_level=1, notes="notes {}".format(number),
                                         speech_type=SpeechType.objects.filter(is_special=False).
                                         order_by("?").first(), presentacion="presentacion {}".format(number),
                                         event=EventECSL.objects.filter(current=True).first())
                                         for number in range(6)]

        return speeaches


    def util_save_objects(self, speeches):
        Speech.objects.all().delete()
        Speech.objects.bulk_create(speeches)


    def control_function(self):
        self.util_save_objects(self.set_asked_time(self.speech_creator()))


    def handle(self, *args, **options):
            self.control_function()
