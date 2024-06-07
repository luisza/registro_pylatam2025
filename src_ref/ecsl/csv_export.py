'''
Created on 2 jun. 2017

@author: luis
'''


import csv
from django.http import HttpResponse
from ecsl.models import Inscription, Payment, PaymentOption, Gustos


def get_datetime(fecha):
    if not fecha:
        return "N/D"
    return fecha


def export_gustos_manias_afiliation2(request, queryset=None, header=[], fields=[], filter=True):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % ("_".join(
        header))
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")

    writer.writerow(header)

    for obj in queryset:
        data_ok = [obj.user.get_full_name()]
        data = []
        d = ""
        for dati in obj.gustos_manias.all():
            d += dati.name + ", "
        data.append(d)
        data.append(obj.observacion_gustos_manias)

        if filter and any(data):
            data_ok += data
            writer.writerow(data_ok)
    return response


def export_gustos_manias_afiliation(request, queryset=None, header=[], fields=[], filter=True):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % ("_".join(
        header))
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")

    writer.writerow(header)

    for obj in queryset:
        data_ok = [obj.user.get_full_name()]
        data = []
        for x in fields:
            x = x.split('__')
            tmp = obj
            for d in x:
                tmp = getattr(tmp, d)
            data.append(tmp)
        if filter and any(data):
            data_ok += data
            writer.writerow(data_ok)
    return response


def export_afiliation(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados.csv"'
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['pago', 'Opción', 'Nombre', 'camiseta', 'identificación',
                     'direccion en su pais',  'género', 'Estado',
                     'nationalidad', 'otra nacionalidad',
                     'born_date', 'institution', 'restrición alimentaria',
                     'consideraciones de salud', 'Gustos y manías', 'Comentario general',
                     'hora de llegada', 'hora de salida', 'medio de transporte', 'lugar de arribo',
                     'observaciones del viaje'
                     ])

    for obj in queryset:
        pays = Payment.objects.filter(user=obj.user).first()
        pago = "No"
        opcion = ' '
        if pays is not None:
            pago = 'Sí' if pays.confirmado else 'No confirmado'

        writer.writerow([
            pago, opcion,
            obj.name, obj.camiseta,
            obj.identification,
            obj.direccion_en_su_pais,
            obj.gender,
            obj.get_status_display(),
            obj.nationality, obj.other_nationality,
            str(obj.born_date) if obj.born_date else " ",
            obj.institution,
            obj.alimentary_restriction,
            obj.health_consideration,
            ",".join([x.name for x in obj.gustos_manias.all()]),
            obj.comentario_general,

            get_datetime(obj.hora_de_llegada),
            get_datetime(obj.hora_de_salida),
            obj.medio_de_transporte,
            obj.lugar_de_arribo,
            obj.observaciones_del_viaje


        ])
    return response


def export_payment(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagos_registrados.csv"'
    if queryset is None:
        queryset = Payment.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Nombre', 'Forma de pago', 'Código de referencia',
                     'confirmado'])

    for obj in queryset:
        writer.writerow([obj.name,
                         str(obj.option),
                         obj.codigo_de_referencia,
                         obj.confirmado

                         ])
    return response


def export_payment_option_stats(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pagos_estadisticas.csv"'
    if queryset is None:
        queryset = Payment.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Nombre', 'cantidad'])

    for paymentoption in PaymentOption.objects.all():
        writer.writerow([
            "(%s) %s" % (paymentoption.tipo, paymentoption.name),
            queryset.filter(option=paymentoption).count()
        ])
    return response


def _export_stats_payments(request, queryset, payments):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados_stats.csv"'
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    gender = list(dict(Inscription.gender_choice).keys())
    writer.writerow(['Descripción', 'Total'] + gender)

    for x in Inscription.PAIS:
        writer.writerow([x[0], queryset.filter(nationality=x[0]).count()] + [queryset.filter(
            gender=gen,
            nationality=x[0]).count() for gen in gender])

    for x in Inscription.CAMISETA:
        writer.writerow([x[0],
                         queryset.filter(camiseta=x[0]).count()
                         ] + [queryset.filter(gender=gen,
                                              camiseta=x[0]).count() for gen in gender])

    writer.writerow(['Total por género', queryset.count()] + [queryset.filter(
        gender=gen).count() for gen in gender])
    return response


def export_stats_payments(request, queryset=None):
    queryset_ins = Inscription.objects.filter(
        user__in=[x['user'] for x in queryset.values('user')])

    return _export_stats_payments(request, queryset=queryset_ins, payments=queryset)


def export_stats_afiliation(request, queryset=None):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrados_stats.csv"'
    if queryset is None:
        queryset = Inscription.objects.all()

    writer = csv.writer(response, delimiter=';', quotechar="'")
    writer.writerow(['Descripción', 'Valor'])
    stats = {}
    for x in Inscription.gender_choice:
        writer.writerow([x[0], queryset.filter(gender=x[0]).count()])

    for x in Inscription.PAIS:
        writer.writerow([x[0], queryset.filter(nationality=x[0]).count()])

    for x in Inscription.CAMISETA:
        writer.writerow([x[0], queryset.filter(camiseta=x[0]).count()])


    writer.writerow(
        ["Confirmados", Payment.objects.filter(confirmado=True).count()])
    writer.writerow(
        ["No Confirmados", Payment.objects.filter(confirmado=False).count()])
    return response
