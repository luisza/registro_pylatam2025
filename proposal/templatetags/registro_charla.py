'''
Created on 11 jun. 2017

@author: luis
'''

from django import template
from django.urls import reverse
from ecsl.models import Payment
from proposal.models import Register_Speech
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag(takes_context=True)
def get_registro(context, schedule):
    request = context['request']
    dia = context['dia'] if 'dia' in context else 1
    dev = {}

    if schedule.speech.pk == 14:
        return

    if not request.user.is_authenticated():
        dev['url'] = reverse('auth_login') + "?next=" + reverse('list_charlas')
        dev['message'] = "Iniciar sesión para registrarse en el evento"
        return dev

    pago = Payment.objects.filter(user=request.user).first()
    if not pago:
        dev['url'] = reverse('index')
        dev['message'] = "Registrese en el encuentro para agendar evento"
        return dev
    registro = Register_Speech.objects.filter(user=request.user,
                                              speech=schedule).first()
    registros = Register_Speech.objects.filter(speech=schedule).count()
    if registros > schedule.room.spaces and not registro:
        dev['url'] = "#"
        dev['message'] = "Sin campos disponibles"
        return dev

    if registro:
        dev['url'] = reverse('desregistrar_charla', kwargs={
                             'pk': registro.pk}) + "?dia=%d" % (dia,)
        dev['message'] = "Desregistrarme"
    else:
        dev['url'] = reverse('registra_charla', kwargs={
                             'pk': schedule.speech.pk}) + "?dia=%d" % (dia,)
        dev['message'] = "Registrarme"
    return dev


@register.simple_tag(takes_context=True)
def get_speech(context, block):
    request = context['request']
    return block.get_speech(user=request.user)
