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
    writer.writerow(['pago', 'Opción', 'Nombre', 'identificación', 'género', 'Estado',
                     'nationalidad', 'otra nacionalidad',
                     'born_date', 'institution', 'restrición alimentaria',
                     'consideraciones de salud', 'Gustos y manías', 'Comentario general'])
   
    for obj in queryset:
        pays = Payment.objects.filter(user=obj.user).first()
        pago="No"
        opcion = ' '
        if pays is not None:
            print(pays)
            opcion = pays.paquete
            pago = 'Sí' if pays.confirmado else 'No confirmado'
            
            
        writer.writerow([
            pago, opcion,
                obj.name, obj.identification, obj.gender,
                     obj.get_status_display(),
                     obj.nationality, obj.other_nationality,
                     str(obj.born_date) if obj.born_date else " ",
                      obj.institution,
                     obj.alimentary_restriction,
                     obj.health_consideration,
                     ",".join([x.name for x in obj.gustos_manias.all()]),
                     obj.comentario_general,
                     ])
    return response

def export_payment(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagos_registrados.csv"'
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

def export_stats_afiliation(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados_stats.csv"'
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Descripción', 'Valor'])
    stats={}
    for x in Inscription.gender_choice:
        writer.writerow([x[0], queryset.filter(gender=x[0]).count() ] )
    
    for x in Inscription.PAIS :
        writer.writerow([x[0], queryset.filter(nationality=x[0]).count() ] )
    
    for x in Inscription.CAMISETA :
        writer.writerow([x[0], queryset.filter(camiseta=x[0]).count() ] )
    
    for x in Payment.PAQUETE :
        writer.writerow([x[0], Payment.objects.filter(paquete=x[0]).count() ] )

    writer.writerow(["Confirmados", Payment.objects.filter(confirmado=True).count() ] )
    writer.writerow(["No Confirmados", Payment.objects.filter(confirmado=False).count() ] )
    return response