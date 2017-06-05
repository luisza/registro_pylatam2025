'''
Created on 2 jun. 2017

@author: luis
'''


import csv
from django.http import HttpResponse
from ecsl.models import Inscription, Payment


def export_afiliation(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados.csv"'
    if queryset is None:
        queryset = Inscription.objects.all()


    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Nombre', 'identificación', 'género', 'Estado'
                     'nationalidad', 'otra nacionalidad',
                     'born_date', 'institution', 'restrición alimentaria',
                     'consideraciones de salud', 'Gustos y manías', 'Comentario general'])
   
    for obj in queryset:
        writer.writerow([obj.name, obj.identification, obj.gender,
                     obj.get_status_display(),
                     obj.nationality, obj.other_nationality,
                     str(obj.born_date), obj.institution,
                     obj.alimentary_restriction,
                     obj.health_consideration,
                     obj.gustos_manias,
                     obj.comentario_general,
                     ])
    return response

def export_payment(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados.csv"'
    if queryset is None:
        queryset = Payment.objects.all()


    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Nombre', 'Paquete', 'Forma de pago', 'Código de referencia',
                     'confirmado'])
   
    for obj in queryset:
        writer.writerow([obj.name, 
                         obj.opcion_paquete,
                         str(obj.option),
                         obj.codigo_de_referencia,
                         obj.confirmado
                         
                     ])   
    return response
