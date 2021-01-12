from django.contrib import admin

# Register your models here.
from ecsl.models import Inscription, Gustos, PaymentOption, Payment, Becas, EventECSL, Package
from ecsl.csv_export import export_payment, export_afiliation,\
    export_stats_afiliation, export_payment_option_stats, export_stats_payments,\
    _export_stats_payments, export_gustos_manias_afiliation,\
    export_gustos_manias_afiliation2
from django.core.mail import send_mail
from ajax_select import make_ajax_form
from async_notifications.register import update_template_context
from async_notifications.utils import send_email_from_template
from django.contrib import messages
from ecsl.pdf import render_pdf


def action_pdf_certificaciones(modeladmin, request, queryset):
    return render_pdf(request, "certificados.pdf", 'ecsl/certificaciones.html', context={
        'object_list': queryset
    })


def action_export_payment(modeladmin, request, queryset):
    return export_payment(request, queryset)


def action_export_afiliation(modeladmin, request, queryset):
    return export_afiliation(request, queryset)


def action_export_stats_afiliation(modeladmin, request, queryset):
    return export_stats_afiliation(request, queryset)


def action_export_payment_option_stats(modeladmin, request, queryset):
    return export_payment_option_stats(request, queryset)


def action_export_stats_payments(modeladmin, request, queryset):
    return export_stats_payments(request, queryset)


def action_export_gustos(modeladmin, request, queryset):
    return export_gustos_manias_afiliation2(request, queryset=queryset,
                                            header=['Nombre', 'Gustos',
                                                    'observaciones'],
                                            fields=['gustos_manias__name', 'observacion_gustos_manias'])


def action_export_condicion_salud(modeladmin, request, queryset):
    return export_gustos_manias_afiliation(request, queryset=queryset,
                                           header=[
                                               'Nombre', 'Condición de salud'],
                                           fields=['health_consideration'])


def action_export_alimentary_restriction(modeladmin, request, queryset):
    return export_gustos_manias_afiliation(request, queryset=queryset,
                                           header=[
                                               'Nombre', 'Restricciones alimenticias'],
                                           fields=['alimentary_restriction'])


def action_reenviar_notificacion(modeladmin, request, queryset):

    for obj in queryset:
        send_mail('Cambio en la suscripción de %s' % (obj.user.get_full_name(),),
                  'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s' % (
            obj.user.get_full_name(),
            obj.option,
            obj.codigo_de_referencia
        ),
            'not-reply@ecsl2017.softwarelibre.ca',
            [obj.option.email],
            fail_silently=False
        )


def action_stats_all_afiliation(modeladmin, request, queryset):
    payments = Payment.objects.none()
    queryset = Inscription.objects.all()
    return _export_stats_payments(request, queryset, payments)


context = [
    ('inscripcion', '''Disponibles:  inscripcion.identification ,
inscripcion.born_date ,
inscripcion.institution,
inscripcion.get_gender_display,
inscripcion.nationality,
inscripcion.other_nationality ,
inscripcion.alimentary_restriction,
inscripcion.health_consideration ,
inscripcion.comentario_general,
inscripcion.camiseta,
inscripcion.hora_de_salida,
inscripcion.medio_de_transporte,
inscripcion.lugar_de_arribo,
inscripcion.observaciones_del_viaje'''),
    ('usuario', '''Disponibles usuario.email, 
    usuario.username, 
    usuario.first_name, 
    usuario.last_name,
    usuario.get_full_name '''),

]
update_template_context("inscripcion.correo",
                        'Mensaje importante del ECSL 2017', context)


def action_enviar_correo_inscripcion(modeladmin, request, queryset):
    for inscripcion in queryset:
        send_email_from_template("inscripcion.correo", [inscripcion.user.email],
                                 context={
                                     'inscripcion': inscripcion,
                                     'usuario': inscripcion.user,
        },
            enqueued=True,
            user=request.user,
            upfile=None)
    messages.success(request, 'Mensajes enviados con éxito')


action_pdf_certificaciones.short_description = "Descargar certificaciones"
action_export_payment.short_description = "Exportar pagos"
action_export_afiliation.short_description = "Exportar registros"
action_export_stats_afiliation.short_description = "Estadísticas de registros"
action_reenviar_notificacion.short_description = "Reenviar notificación de pago"
action_export_payment_option_stats.short_description = "Estadisticas según tipo de pago"
action_export_stats_payments.short_description = "Estadísticas de pagos"
action_stats_all_afiliation.short_description = "Estadisticas todos los afiliados"


action_export_gustos.short_description = "Exportar Gustos"
action_export_condicion_salud.short_description = "Exportar Condiciones de salud"
action_export_alimentary_restriction.short_description = "Restricciones alimentarias"
action_enviar_correo_inscripcion.short_description = "Enviar correo"


@admin.register(Inscription)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'gender', 'status')
    list_filter = ('nationality', 'gender', 'status',
                   'gustos_manias')
    search_fields = (
        'user__first_name',
        'user__last_name',
    )
    actions = [action_enviar_correo_inscripcion,
               action_export_afiliation, action_export_stats_afiliation,
               action_export_gustos,
               action_export_condicion_salud,
               action_export_alimentary_restriction,
               action_pdf_certificaciones]
    form = form = make_ajax_form(Inscription, {'user': 'users'})


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'option',
                    'confirmado', 'codigo_de_referencia')
    list_filter = ('confirmado', 'option')
    search_fields = (
        'user__first_name',
        'user__last_name',
    )
    actions = [action_export_payment,
               action_reenviar_notificacion,
               action_export_payment_option_stats,
               action_export_stats_payments,
               action_stats_all_afiliation]
    form = make_ajax_form(Payment, {'user': 'users'})

    def save_model(self, request, obj, form, change):
        dev = admin.ModelAdmin.save_model(self, request, obj, form, change)
        ins = Inscription.objects.filter(user=obj.user).first()
        if ins and obj.confirmado:
            ins.status = 2
            ins.save()
        return dev


admin.site.register(Gustos)
admin.site.register(PaymentOption)
admin.site.register(Becas)
admin.site.register(EventECSL)
admin.site.register(Package)

admin.site.site_header = "ECSL Administración"
