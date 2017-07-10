'''
Created on 5 jun. 2017

@author: luis
'''
from django.views.generic.list import ListView
from proposal.models import SpeechSchedule, Topic, Speech, Register_Speech,\
    BlockSchedule
import datetime
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.urls.base import reverse
from ecsl.models import Payment
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator


class CharlaContext:
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)

        dia_1_start = datetime.datetime(
            day=21, month=7, year=2017, hour=0, minute=0)
        dia_1_end = datetime.datetime(
            day=21, month=7, year=2017, hour=23, minute=59)

        dia_2_start = datetime.datetime(
            day=22, month=7, year=2017, hour=0, minute=0)
        dia_2_end = datetime.datetime(
            day=22, month=7, year=2017, hour=23, minute=59)

        queryset = context['object_list']

        charlas = {
            'dia1': queryset.filter(
                start_time__gte=dia_1_start,
                start_time__lte=dia_1_end,
            ).order_by('start_time'),
            'dia2': queryset.filter(
                start_time__gte=dia_2_start,
                start_time__lte=dia_2_end,
            ).order_by('start_time')

        }

        try:
            dia = int(self.request.GET.get('dia', '1'))
            if dia not in [1, 2]:
                raise
        except:
            dia = 1

        context['object_list'] = charlas["dia%s" % (dia)]
        context['dia'] = dia
        context['tipos'] = Topic.objects.all()
        return context


class Charlas(CharlaContext, ListView):
    model = BlockSchedule
    order_by = "start_time"


@method_decorator(login_required, name='dispatch')
class MyAgenda(CharlaContext, ListView):
    model = BlockSchedule
    template_name = 'proposal/mi_agenda.html'
    order_by = "start_time"

    def dispatch(self, request, *args, **kwargs):
        pago = Payment.objects.filter(user=request.user).first()
        error = False
        try:
            inscription = request.user.inscription
        except:
            error = True
        if not pago:
            error = True

        if error or not inscription:
            messages.error(
                request, "Lo lamentamos, primero actualiza tus datos y procede con el registro")
            return redirect(reverse('index'))

        return ListView.dispatch(self, request, *args, **kwargs)


class CharlaDetail(DetailView):
    model = Speech

    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)

        context['schedule'] = get_object_or_404(
            SpeechSchedule, speech=context['object'])
        return context


@login_required
def register_user_to_speech(request, pk):
    speech = get_object_or_404(Speech, pk=pk)
    schedule = get_object_or_404(SpeechSchedule, speech=speech)
    pago = Payment.objects.filter(user=request.user).first()

    try:
        dia = int(request.GET.get('dia', '1'))
        if dia not in [1, 2]:
            raise
    except:
        dia = 1

    error = False
    try:
        inscription = request.user.inscription
    except:
        error = True
    if not pago:
        error = True
    if not schedule:
        error = True
    if error or not inscription:
        messages.error(
            request, "Lo lamentamos, primero actualiza tus datos y luego procede con el registro")
        return redirect(reverse('index'))

    registros = Register_Speech.objects.filter(speech=schedule).count()
    if registros > schedule.room.spaces:
        messages.error(
            request, "Lo lamentamos no hay espacio disponibles en esta actividad")
        return redirect(reverse('list_charlas') + "?dia=%d" % (dia,))

    registros = Register_Speech.objects.filter(user=request.user)

    registros = registros.filter(Q(
        speech__start_time__lte=schedule.start_time,
        speech__end_time__gt=schedule.start_time) | Q(
        speech__start_time__lt=schedule.end_time,
        speech__end_time__gt=schedule.end_time
    )

    ).count()

    if registros > 0:
        messages.error(
            request, "Lo lamentamos hay un choque de horarios en su agenda")
        return redirect(reverse('list_charlas') + "?dia=%d" % (dia,))

    Register_Speech.objects.create(user=request.user,
                                   speech=schedule)

    messages.success(
        request, "Felicidades ha sido registrado en %s" % (speech.title))
    return redirect(reverse('list_charlas') + "?dia=%d" % (dia,))


@login_required
def desregistrar_charla(request, pk):
    try:
        dia = int(request.GET.get('dia', '1'))
        if dia not in [1, 2]:
            raise
    except:
        dia = 1
    registro = Register_Speech.objects.filter(pk=pk, user=request.user).first()
    if registro:
        registro.delete()
        messages.success(request, "Felicidades ha sido eliminado su registro")
    else:
        messages.error(
            request, "Registro no encontrado, ¿es usted el usuario correcto?")
    return redirect(reverse('list_charlas') + "?dia=%d" % (dia,))
