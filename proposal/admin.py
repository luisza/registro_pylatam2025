from django.contrib import admin

# Register your models here.

from proposal.models import SpeechType, Topic, Speech, SpeechSchedule, Room,\
    Register_Speech
from django.http.response import HttpResponse
import csv

import io
import zipfile
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

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
        files.append((  query.title, csvfile ) )
    
    with zipfile.ZipFile(response, 'w') as f:
        for i, file in files:
            file.seek(0)
            f.writestr("{}.csv".format(i), file.getvalue())
    
    return response  

action_export_register_list.short_description = "Descargar usuarios registrados"

class SpeechAdmin(admin.ModelAdmin):
    list_display = ['speaker_name', 'title', 'skill_level', 'registrados_cuenta']
    list_filter = ['topic', 'speech_type']
    actions = [action_export_register_list]
    search_fields = (
            'title',
            'user__first_name',
            'user__last_name',
        )
    readonly_fields = ('registrados_cuenta', 'get_registration_list',)


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

admin.site.register(Speech, SpeechAdmin)
admin.site.register([SpeechType, Topic, SpeechSchedule, Room])
