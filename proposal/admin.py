from django.contrib import admin, messages

# Register your models here.

from proposal.models import SpeechType, Topic, Speech, SpeechSchedule, Room,\
    Register_Speech, BlockSchedule
from django.http.response import HttpResponse
import csv

import io
import zipfile
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from ajax_select.helpers import make_ajax_form
from async_notifications.register import update_template_context
from async_notifications.utils import send_email_from_template


context = [
    ('inscripcion', '''Disponibles:  actividad.speaker_information,
 actividad.title,
 actividad.description,
 actividad.topic,
 actividad.audience,
 actividad.skill_level,
 actividad.notes,
 actividad.speech_type,
 actividad.presentacion'''),
    ('usuario', '''Disponibles usuario.email, 
    usuario.username, 
    usuario.first_name, 
    usuario.last_name,
    usuario.get_full_name '''),

]
update_template_context("charla.expositor",
                        'Mensaje importante sobre su actividad en el ECSL 2017', context)


def action_enviar_correo_charla(modeladmin, request, queryset):
    for prop in queryset:
        send_email_from_template("charla.expositor", [prop.user.email],
                                 context={
                                     'actividad': prop,
                                     'usuario': prop.user,
        },
            enqueued=True,
            user=request.user,
            upfile=None)
    messages.success(request, 'Mensajes enviados con éxito')


action_enviar_correo_charla.short_description = "Enviar correo a expositores"


context = [
    ('inscripcion', '''Disponibles:  actividad.speaker_information,
 actividad.title,
 actividad.description,
 actividad.topic,
 actividad.audience,
 actividad.skill_level,
 actividad.notes,
 actividad.speech_type,
 actividad.presentacion'''),
    ('usuario', '''Disponibles usuario.email, 
    usuario.username, 
    usuario.first_name, 
    usuario.last_name,
    usuario.get_full_name '''),
    ('expositor', '''Disponibles usuario.email, 
    usuario.username, 
    usuario.first_name, 
    usuario.last_name,
    usuario.get_full_name '''),
    ('agenta', """Disponibles: agenda.start_time
agenda.end_time
agenda.speech
agenda.room""")

]
update_template_context("charla.participante",
                        'Mensaje importante sobre su actividad en el ECSL 2017', context)


def action_enviar_correo_charla_participantes(modeladmin, request, queryset):
    for prop in queryset:
        for participa in Register_Speech.objects.filter(speech__speech=prop):
            send_email_from_template("charla.participante", [prop.user.email],
                                     context={
                                     'actividad': prop,
                                     'usuario': participa.user,
                                     'expositor': prop.user,
                                     'agenda': participa.speech
                                     },
                                     enqueued=True,
                                     user=request.user,
                                     upfile=None)
    messages.success(request, 'Mensajes enviados con éxito')


action_enviar_correo_charla_participantes.short_description = "Enviar correo a participantes"


def action_export_register_list(modeladmin, request, queryset):
    if queryset is None:
        queryset = Speech.objects.all()
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="registrados_en_charla.zip"'

    files = []
    for query in queryset:
        csvfile = io.StringIO()
        writer = csv.writer(csvfile, delimiter=';', quotechar="'")
        writer.writerow(['Nombre', 'correo', 'Firma'])
        registros = Register_Speech.objects.filter(speech__speech=query)
        for regs in registros:
            writer.writerow([regs.user.get_full_name(), regs.user.email, ' '])
        files.append((query.title, csvfile))

    with zipfile.ZipFile(response, 'w') as f:
        for i, file in files:
            file.seek(0)
            f.writestr("{}.csv".format(i), file.getvalue())

    return response


action_export_register_list.short_description = "Descargar usuarios registrados"


class AgendaFilter(admin.SimpleListFilter):
    title = "En agenda"
    parameter_name = 'agenda'

    def lookups(self, request, model_admin):
        return (
            ('1', "En agenda"),
            ('2', 'Propuesta'),
        )

    def queryset(self, request, queryset):
        pks = [x['speech']
               for x in SpeechSchedule.objects.all().values('speech')]
        if self.value() == '1':
            return queryset.filter(pk__in=pks)
        if self.value() == '2':
            return queryset.exclude(pk__in=pks)


class CharlistaConfirmadoFilter(admin.SimpleListFilter):
    title = "Charlista confirmado"
    parameter_name = 'agenda'

    def lookups(self, request, model_admin):
        return (
            ('1', "Confirmado"),
            ('2', 'No confirmado'),
        )

    def queryset(self, request, queryset):
        pks = [x['speech']
               for x in SpeechSchedule.objects.all().values('speech')]
        if self.value() == '1':
            return queryset.filter(pk__in=pks)
        if self.value() == '2':
            return queryset.exclude(pk__in=pks)


class SpeechAdmin(admin.ModelAdmin):
    list_display = ['speaker_name', 'title',
                    'skill_level', 'registrados_cuenta']
    list_filter = [AgendaFilter, 'topic', 'speech_type']
    actions = [action_enviar_correo_charla,
               action_enviar_correo_charla_participantes,
               action_export_register_list]
    search_fields = (
        'title',
        'user__first_name',
        'user__last_name',
    )
    readonly_fields = ('registrados_cuenta', 'get_registration_list',)
    form = make_ajax_form(Speech, {'user': 'users'})

    def registrados_cuenta(self, instance):
        regs = Register_Speech.objects.filter(speech__speech=instance)
        return regs.count()
    registrados_cuenta.short_description = "# registrados"

    def get_registration_list(self, instance):

        regs = Register_Speech.objects.filter(speech__speech=instance)

        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line.user.get_full_name(),) for line in regs),
        ) or mark_safe("<span class='errors'>No hay personas registradas en esta charla.</span>")

    get_registration_list.short_description = "Lista de registrados"


class ScheduleAdmin(admin.ModelAdmin):
    form = make_ajax_form(SpeechSchedule, {'speech': 'charlas'})
    search_fields = (
        'speech__title',
        'speech__user__first_name',
        'speech__user__last_name',
    )

    ordering = ['start_time']
    list_filter = ['speech__speech_type', 'room']


class BlockScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_speech', 'text', 'color')
    list_editable = ('color', )


admin.site.register(Speech, SpeechAdmin)
admin.site.register(SpeechSchedule, ScheduleAdmin)
admin.site.register([SpeechType, Topic, Room])
admin.site.register(BlockSchedule, BlockScheduleAdmin)
