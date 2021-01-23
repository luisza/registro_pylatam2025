from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ecsl.models import EventECSL


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    color = models.CharField(max_length=10, default="#fff")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Temática"
        verbose_name_plural = "Temáticas"


class SpeechTime(models.Model):
    name = models.CharField(max_length=40, verbose_name=_("Name"), default=_("Basic speech"))
    time = models.IntegerField(default=10, verbose_name=_("Time (in minutes)"))

    def __str__(self):
        return f"%s (%d minutes)" % (self.name, self.time)

    class Meta:
        verbose_name = _("Activity Duration")
        verbose_name_plural = _("Activity Duration")


class SpeechType(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de actividad"
        verbose_name_plural = "Tipos de actividad"


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    speaker_information = models.TextField(
        verbose_name=_("Speaker_information"))
    title = models.TextField(verbose_name=_("Speech Title"))
    description = models.TextField(verbose_name=_("Description"))
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              verbose_name=_("Topic"))
    audience = models.TextField(verbose_name=_("Audience"))
    skill_level = models.PositiveIntegerField(
        choices=SKILL_LEVEL.choices, default=SKILL_LEVEL.EVERYONE,
        verbose_name=_("Skill level required"))
    notes = models.TextField(blank=True,
                             verbose_name=_("Notes for audience"))
    speech_type = models.ForeignKey(SpeechType, on_delete=models.CASCADE, verbose_name=_("Speech Type"))

    presentacion = models.FileField(upload_to='presentaciones/',
                                    verbose_name=_("Presentation"),
                                    null=True, blank=True)
    event = models.ForeignKey(EventECSL, default="", on_delete=models.CASCADE, verbose_name=_("Event"))
    time_asked = models.ForeignKey(SpeechTime, null=True, on_delete=models.CASCADE, related_name='time_asked', verbose_name=_("Duration"))
    time_given = models.ForeignKey(SpeechTime, null=True, on_delete=models.CASCADE, related_name='time_given', verbose_name=_("Duration Assigned"))
    is_scheduled = models.BooleanField(default=False, verbose_name=_('is Scheduled'))

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
        # permissions = (
        #     ("view_speech", "Can see available Speech"),
        # )

        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    spaces = models.SmallIntegerField(default=30, verbose_name=_('Spaces'))
    map = models.ImageField(upload_to="mapa", null=True, blank=True, verbose_name=_('Map'))
    event = models.ForeignKey(EventECSL, on_delete=models.CASCADE, verbose_name=_("Event"), null=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


class Register_Speech(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speech = models.ForeignKey('SpeechSchedule', on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user.get_full_name(), self.speech.speech.title)

    class Meta:
        verbose_name = "Registro en actividad"
        verbose_name_plural = "Registros en actividades"


class SpeechSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speech = models.ForeignKey(Speech, on_delete=models.CASCADE, null=True, blank=True)
    special = models.ForeignKey('SpecialActivity', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('Room', default="", on_delete=models.CASCADE)

    def __str__(self):
        return "(%s %s) %s" % (self.start_time.strftime("%Y-%m-%d %H:%M"),
                                     self.end_time.strftime("%Y-%m-%d %H:%M"),
                                     self.room.name)

    @property
    def title(self):
        return self.room.name + " "+str(self.start_time)+" "+str(self.end_time)

    def registros(self):
        regs = Register_Speech.objects.filter(speech=self).count()
        total = self.room.spaces - regs

        dev = "Lleno"
        if total > 0:
            dev = "Hay %d espacios" % (total,)

        return dev

    class Meta:
        verbose_name = "Horario de actividad"
        verbose_name_plural = "Horarios de actividades"


class SpecialActivity(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    time = models.ForeignKey(SpeechTime, null=True, on_delete=models.CASCADE,verbose_name=_("Duration Assigned"))
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    room = models.ForeignKey('Room', default="", on_delete=models.CASCADE, verbose_name=_("Room"))
    event = models.ForeignKey(EventECSL, default="", on_delete=models.CASCADE, verbose_name=_("Event"))
    is_scheduled = models.BooleanField(default=False, verbose_name=_('is Scheduled'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actividad Especial"
        verbose_name_plural = "Actividades Especiales"


class BlockSchedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_speech = models.BooleanField()
    text = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=10)
    room = models.ForeignKey('Room', default="", on_delete=models.CASCADE, verbose_name=_("Room"))

    def __str__(self):
        return "%s %s" % (self.start_time.strftime("%Y-%m-%d %H:%M"),
                          self.end_time.strftime("%Y-%m-%d %H:%M"),)

    def get_speech(self, user=None):
        query = SpeechSchedule.objects.filter(
            start_time=self.start_time,
        )
        if user:
            query = query.filter(register_speech__user=user)

        return query.order_by('start_time')

    class Meta:
        verbose_name = "Bloque de horario"
        verbose_name_plural = "Bloques de horarios"
