'''
Created on 5 jun. 2017

@author: luis
'''
import json
from django.utils import timezone
from django.views.generic.list import ListView
from proposal.models import SpeechSchedule, Topic, Speech, Register_Speech, \
    BlockSchedule, SpeechType, SpecialActivity
import datetime
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls.base import reverse
from ecsl.models import Payment, EventECSL
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from proposal.models import Room
from ecsl.forms import scheduleForm
from proposal.forms import TopicForm, TypeForm, SpecialActivityForm, RoomsCreateForm


def dayAmout(date1, date2):
    difference = date1 - date2
    return int(difference.days) + 1


class CharlaContext:
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        current_event = EventECSL.objects.filter(current=True).first()

        def daterange(date1, date2):
            days = []
            for n in range(int((date2 - date1).days) + 1):
                days.append(date1 + datetime.timedelta(n))
            return days

        queryset = context['object_list']
        charlasDic = {}
        counter = 1
        for day in daterange(current_event.start_date, current_event.end_date):
            name = 'dia' + str(counter)
            day_start = datetime.datetime(day.year, day.month, day.day, 0, 0)
            day_end = datetime.datetime(day.year, day.month, day.day, 23, 59)
            counter += 1
            charlasDic[name] = queryset.filter(start_time__gte=day_start, start_time__lte=day_end).order_by(
                'start_time')

        try:
            dia = int(self.request.GET.get('dia', '1'))
            if dia not in range(1, len(charlasDic) + 1):
                raise
        except:
            dia = 1

        days = []
        for day in daterange(current_event.start_date, current_event.end_date):
            # txt = str(day.day)+" de "+str(day.strftime('%B'))
            # days.append(txt)
            days.append(day)

        rooms_list = Room.objects.filter(event=current_event)
        rooms_names = {}
        counter = 1
        for room in rooms_list:
            rooms_names[str(counter)] = room.name
            counter += 1
        try:
            sala = int(self.request.GET.get('sala', '1'))
            if sala not in range(1, len(rooms_list) + 1):
                raise
        except:
            sala = 1

        speeches = Speech.objects.filter(event=current_event, is_scheduled=False)
        special = SpecialActivity.objects.filter(event=current_event, is_scheduled=False)
        context['dayList'] = days
        context['object_list'] = charlasDic["dia%s" % (dia)]
        context['dia'] = dia
        context['topics'] = Topic.objects.all()
        context['types'] = SpeechType.objects.all()
        print(charlasDic["dia%s" % (dia)])
        context['diaActual'] = days[dia - 1]
        context['form'] = scheduleForm()
        context['speeches'] = speeches
        context['topicForm'] = TopicForm()
        context['typeForm'] = TypeForm()
        context['specialForm'] = SpecialActivityForm()
        context['specialActivity'] = special
        context['rooms_list'] = rooms_list
        context['sala'] = sala
        context['room_name'] = rooms_names[str(sala)]
        context['room_id'] = rooms_list[sala - 1].id
        context['room_form'] = RoomsCreateForm()
        return context


class Charlas(CharlaContext, ListView):
    model = BlockSchedule
    order_by = "start_time"

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            messages.success(
                self.request, _("Sorry, we need an event to display the schedule"))
            return redirect('sineventos/')
        return super(Charlas, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('form_id'):
                if request.POST['form_id'] == 'delete':
                    block = BlockSchedule.objects.filter(id=request.POST['block']).first()
                    schedule = SpeechSchedule.objects.filter(start_time=block.start_time, room=request.POST['room']).first()
                    if block.is_speech:
                        speech = schedule.speech
                        speech.is_scheduled = False
                        speech.save()
                    block.delete()
                    schedule.delete()

            form = scheduleForm(request.POST)
            if request.POST.get('agenda'):
                result = json.loads(request.POST['agenda'])
                for activities in result:
                    blockValid = False
                    scheduleValid = False

                    speechSchedule = SpeechSchedule(start_time=timezone.datetime.strptime(activities['start_time'],
                                                                                          "%Y-%m-%d %H:%M:%S"),
                                                    end_time=timezone.datetime.strptime(
                                                        activities['end_time'], "%Y-%m-%d %H:%M:%S"),
                                                    speech=Speech.objects.filter(
                                                        id=int(activities['pk_speech'])).first(),
                                                    room=Room.objects.filter(id=int(activities['room'])).first(), )
                    speech = SpeechSchedule.objects.filter(room=speechSchedule.room,
                                                           start_time__lt=speechSchedule.end_time,
                                                           end_time__gt=speechSchedule.start_time).first()
                    sameSpeech = SpeechSchedule.objects.filter(room=speechSchedule.room,
                                                               start_time=speechSchedule.start_time,
                                                               end_time=speechSchedule.end_time).first()
                    if not speech and not sameSpeech and speechSchedule.start_time <= speechSchedule.end_time:
                        speechSchedule.save()
                        scheduleValid = True

                    blockSchedule = BlockSchedule(start_time=timezone.datetime.strptime(
                        activities['start_time'], "%Y-%m-%d %H:%M:%S"),
                        end_time=timezone.datetime.strptime(
                            activities['end_time'], "%Y-%m-%d %H:%M:%S"),
                        is_speech=bool(activities['is_speech']),
                        text=activities['description'],
                        color=activities['color'],
                        room=speechSchedule.room)
                    block = BlockSchedule.objects.filter(start_time__lt=blockSchedule.end_time,
                                                         end_time__gt=blockSchedule.start_time,
                                                         room=speechSchedule.room).first()
                    sameBlock = BlockSchedule.objects.filter(start_time=blockSchedule.start_time,
                                                             end_time=blockSchedule.end_time,
                                                             room=speechSchedule.room).first()

                    if not block and not sameBlock and blockSchedule.start_time <= blockSchedule.end_time:
                        blockSchedule.save()
                        blockValid = True

                    if activities['is_speech'] and blockValid and scheduleValid:
                        speech = Speech.objects.filter(id=int(activities['pk_speech'])).first()
                        speech.is_scheduled = True
                        speech.save()

            return redirect(reverse('list_charlas'))


@method_decorator(login_required, name='dispatch')
class MyAgenda(CharlaContext, ListView):
    model = BlockSchedule
    template_name = 'proposal/mi_agenda.html'
    order_by = "start_time"

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            messages.success(
                self.request, _("Sorry, we need an event to display the schedule"))
            return redirect('sineventos/')
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

        if pago.confirmado == False:
            messages.error(
                request, _("The payment is still pending to be confirmed"))
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
    current_event = EventECSL.objects.filter(current=True).first()
    speech = get_object_or_404(Speech, pk=pk)
    fecha = datetime.datetime(int(request.GET['year']), int(request.GET['month']), int(request.GET['day']),
                              int(request.GET['hour']), int(request.GET['minute']), int(request.GET['second']))
    schedule = get_object_or_404(SpeechSchedule, speech=speech, start_time=fecha)
    pago = Payment.objects.filter(user=request.user).first()

    try:
        dia = int(request.GET.get('dia', '1'))
        if dia not in (1, dayAmout(current_event.end_date, current_event.start_date)):
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
    if pago.confirmado == False:
        messages.error(
            request, _("The payment is still pending to be confirmed"))
        return redirect(reverse('list_charlas') + "?dia=%d" % (dia,))

    registros = Register_Speech.objects.filter(speech=schedule).count()
    if registros >= schedule.room.spaces:
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
    current_event = EventECSL.objects.filter(current=True).first()
    try:
        dia = int(request.GET.get('dia', '1'))
        if dia not in (1, dayAmout(current_event.end_date, current_event.start_date)):
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
