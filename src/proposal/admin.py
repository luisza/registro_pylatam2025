from django.contrib import admin, messages

# Register your models here.
from django.contrib.auth.models import Permission

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
from ecsl.pdf import render_pdf

from proposal.models import SpecialActivity

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


def action_export_pdf_register_list(modeladmin, request, queryset):
    query = []

    for activity in queryset:
        query.append({
            'activity': activity,
            'participants': Register_Speech.objects.filter(speech__speech=activity)
        })
        # print(activity)
        # print([(x.pk, x)
        # for x in Register_Speech.objects.filter(speech__speech=activity)])

    return render_pdf(request, 'lista_participantes.pdf',
                      'speech/lista_participantes_pdf.html', context={
            'object_list': query
        })


action_export_pdf_register_list.short_description = "Lista de participación pdf"


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
                    'skill_level', 'registrados_cuenta', 'en_agenda']
    list_filter = [AgendaFilter,
                   'speechschedule__room', 'topic', 'speech_type']
    actions = [action_enviar_correo_charla,
               action_enviar_correo_charla_participantes,
               action_export_register_list,
               action_export_pdf_register_list]
    search_fields = (
        'title',
        'user__first_name',
        'user__last_name',
    )
    readonly_fields = ('registrados_cuenta',
                       'get_registration_list', 'en_agenda')
    form = make_ajax_form(Speech, {'user': 'users'})

    def registrados_cuenta(self, instance):
        regs = Register_Speech.objects.filter(speech__speech=instance)
        return regs.count()

    registrados_cuenta.short_description = "# registrados"

    def en_agenda(self, instance):
        schedule = SpeechSchedule.objects.filter(speech=instance).first()
        if not schedule:
            return "No agendada"
        return "%s -- %s" % (
            schedule.start_time.strftime("%b %d %H:%M"),
            schedule.end_time.strftime("%H:%M")
        )

    en_agenda.short_description = "Horario"
    en_agenda.admin_order_field = '-speechschedule__start_time'

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

    list_display = ('title', 'start_time', 'end_time', 'room')
    list_editable = ('start_time', 'end_time', 'room')


class BlockScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_speech', 'text', 'color')
    list_editable = ('color',)


def action_ud_esta_aqui(modeladmin, request, queryset):
    template_path = 'ecsl/ud_esta_aqui.html'
    context = {
        'object_list': queryset
    }

    return render_pdf(request, 'ud_esta_aqui.pdf',
                      'ecsl/ud_esta_aqui.html',
                      context=context
                      )
    action_ud_esta_aqui.short_description = "Usted está aquí"


class RoomAdmin(admin.ModelAdmin):
    actions = [action_ud_esta_aqui]


admin.site.register(SpecialActivity)
admin.site.register(Speech, SpeechAdmin)
admin.site.register(SpeechSchedule, ScheduleAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register([SpeechType, Topic])
admin.site.register(BlockSchedule, BlockScheduleAdmin)
admin.site.register(Permission)
