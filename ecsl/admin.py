from django.contrib import admin

# Register your models here.
from ecsl.models import Inscription, Gustos, PaymentOption, Payment, Becas
from ecsl.csv_export import export_payment, export_afiliation,\
    export_stats_afiliation
from django.core.mail import send_mail
from ajax_select import make_ajax_form

def action_export_payment(modeladmin, request, queryset):
    return export_payment(request, queryset)

def action_export_afiliation(modeladmin, request, queryset):
    return export_afiliation(request, queryset)

def action_export_stats_afiliation(modeladmin, request, queryset):
    return export_stats_afiliation(request, queryset)


def action_reenviar_notificacion(modeladmin, request, queryset):
    
    for obj in queryset:
        send_mail('Cambio en la suscripción de %s'%(obj.user.get_full_name(),),
            'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s'%(
                obj.user.get_full_name(),
                obj.option,
                obj.codigo_de_referencia
                ),
            'not-reply@ecsl2017.softwarelibre.ca',
            [obj.option.email],
             fail_silently=False
            )


action_export_payment.short_description = "Exportar pagos"
action_export_afiliation.short_description = "Exportar registros"
action_export_stats_afiliation.short_description = "Estadísticas de registros"
action_reenviar_notificacion.short_description = "Reenviar notificación de pago"

@admin.register(Inscription)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'gender', 'status' )
    list_filter = ('nationality', 'gender', 'status')
    search_fields = (
            'user__first_name',
            'user__last_name',
        )
    actions = [action_export_afiliation, action_export_stats_afiliation]
    form = form = make_ajax_form(Inscription, {'user': 'users'})

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'option', 'opcion_paquete', 'confirmado', 'codigo_de_referencia' )
    list_filter = ('confirmado', 'option', 'paquete')
    search_fields = (
            'user__first_name',
            'user__last_name',
        )
    actions=[action_export_payment,
             action_reenviar_notificacion]
    form = make_ajax_form(Payment, {'user': 'users'})

admin.site.register(Gustos)
admin.site.register(PaymentOption)
admin.site.register(Becas)

admin.site.site_header = "ECSL Administración"