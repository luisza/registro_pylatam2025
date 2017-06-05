from django.contrib import admin

# Register your models here.
from ecsl.models import Inscription, Gustos, PaymentOption, Payment, Becas
from ecsl.csv_export import export_payment, export_afiliation,\
    export_stats_afiliation

def action_export_payment(modeladmin, request, queryset):
    return export_payment(request, queryset)

def action_export_afiliation(modeladmin, request, queryset):
    return export_afiliation(request, queryset)

def action_export_stats_afiliation(modeladmin, request, queryset):
    return export_stats_afiliation(request, queryset)

action_export_payment.short_description = "Exportar pagos"
action_export_afiliation.short_description = "Exportar registros"
action_export_stats_afiliation.short_description = "Estadísticas de registros"

@admin.register(Inscription)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'gender', 'status' )
    list_filter = ('nationality', 'gender', 'status')
    search_fields = (
            'user__first_name',
            'user__last_name',
        )
    actions = [action_export_afiliation, action_export_stats_afiliation]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'option', 'opcion_paquete', 'confirmado', 'codigo_de_referencia' )
    list_filter = ('confirmado', 'option', 'paquete')
    search_fields = (
            'user__first_name',
            'user__last_name',
        )
    actions=[action_export_payment]

admin.site.register(Gustos)
admin.site.register(PaymentOption)
admin.site.register(Becas)

admin.site.site_header = "ECSL Administración"