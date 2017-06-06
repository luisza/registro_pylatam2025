from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class SpeechType(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class Speech(models.Model):

    class SKILL_LEVEL:
        EVERYONE = 1
        NOVICE = 2
        INTERMEDIATE = 3
        ADVANCED = 4

        choices = [
            (EVERYONE, _('everyone')),
            (NOVICE, _('novice')),
            (INTERMEDIATE, _('intermediate')),
            (ADVANCED, _('advanced')),
        ]

    user = models.ForeignKey(User)
    speaker_information = models.TextField(
        verbose_name=_("Speaker_information"))
    title = models.TextField(verbose_name=_("Speech Title"))
    description = models.TextField(verbose_name=_("Description"))
    topic = models.ForeignKey(Topic, verbose_name=_("Topic"))
    audience = models.TextField(verbose_name=_("Audience"))
    skill_level = models.PositiveIntegerField(
        choices=SKILL_LEVEL.choices, default=SKILL_LEVEL.EVERYONE,
        verbose_name=_("Skill level required"))
    notes = models.TextField(blank=True,
                             verbose_name=_("Notes for audience"))
    speech_type = models.ForeignKey(SpeechType, verbose_name=_("Speech Type"))
    
    presentacion = models.FileField(upload_to='presentaciones/', null=True, blank=True)


    @property
    def speaker_name(self):
        return self.user.get_full_name()

    @property
    def speaker_registered(self):
        dev = False
        try:
            dev = self.user.payment.confirmado
        except:
            pass
        return dev
            
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('pk',)
        permissions = (
            ("view_speech", "Can see available Speech"),
            )

class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    spaces = models.SmallIntegerField(default=30)
    
    def __str__(self):
        return self.name
    
class SpeechSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speech = models.ForeignKey(Speech)
    room = models.ForeignKey(Room)
    
    def __str__(self):
        return "(%s %s) %s en %s"%(self.start_time.strftime("%Y-%m-%d %H:%M"), 
                   self.end_time.strftime("%Y-%m-%d %H:%M"), 
                   self.speech.title, self.room.name )
    
class Register_Speech(models.Model):
    user = models.ForeignKey(User)
    speech = models.ForeignKey(SpeechSchedule)
    
    def __str__(self):
        return "%s %s"%(self.user.get_full_name(), self.speech.title)