'''
Created on 5 jun. 2017

@author: luis
'''
import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ecsl.forms import scheduleForm
from ecsl.models import Payment, EventECSL
from proposal.forms import TopicForm, TypeForm, SpecialActivityForm, RoomsCreateForm
from proposal.models import Room
from proposal.models import SpeechSchedule, Topic, Speech, Register_Speech, \
    BlockSchedule, SpeechType, SpecialActivity

SPECIAL_ACTIVITY_COLOR = "#cccccc"


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
        context['types'] = SpeechType.objects.filter(is_special=False)
        context['types_serializer'] = serializers.serialize('json', SpeechType.objects.filter(is_special=False))
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
        speeches = Speech.objects.filter(event=current_event)
        special = SpecialActivity.objects.filter(event=current_event)
        context['activities_dic'] = json.dumps(build_activities_dic(speeches, special))
        context['stored_activities_dic'] = json.dumps(
            build_stored_activities_dic(charlasDic["dia%s" % (dia)], rooms_names[str(sala)]))
        return context


def build_activities_dic(speeches, special_activities):
    activities_dic = {}
    for special_activity in special_activities:
        temp_dic = {}
        temp_key = "0-" + str(special_activity.id)
        temp_dic['name'] = special_activity.name
        temp_dic['desc'] = special_activity.message
        temp_dic['color'] = SPECIAL_ACTIVITY_COLOR
        temp_dic["is_speech"] = ""
        temp_dic["time"] = special_activity.type.time
        temp_dic["type"] = special_activity.type.pk
        temp_dic["activity_pk"] = special_activity.id
        temp_dic["is_scheduled"] = special_activity.is_scheduled
        activities_dic[temp_key] = temp_dic

    for speech in speeches:
        temp_dic = {}
        temp_key = "1-" + str(speech.id)
        temp_dic["title"] = speech.title
        temp_dic["color"] = speech.topic.color
        temp_dic["time"] = speech.speech_type.time
        temp_dic["is_speech"] = "true"
        temp_dic["activity_pk"] = speech.pk
        temp_dic["speech_pk"] = speech.pk
        temp_dic["speech_type"] = speech.speech_type.pk
        temp_dic['speech_topic'] = speech.topic.pk
        temp_dic["desc"] = "none"
        temp_dic["is_scheduled"] = speech.is_scheduled
        activities_dic[temp_key] = temp_dic

    return activities_dic


def build_stored_activities_dic(object_list, room):
    activities_dic = {}
    for obj in object_list:
        if obj.room.name == room:
            for speech in obj.get_speech():
                temp_dic = {}
                temp_dic["room_pk"] = speech.room.pk
                temp_dic["obj_pk"] = obj.pk

                if obj.is_speech:
                    temp_dic["start_datetime"] = timezone.localtime(speech.start_time).strftime("%Y-%m-%d %H:%M:%S")
                    temp_dic["end_datetime"] = timezone.localtime(speech.end_time).strftime("%Y-%m-%d %H:%M:%S")
                    temp_dic["start_time"] = timezone.localtime(speech.start_time).strftime("%H:%M")
                    temp_dic["start_hour"] = timezone.localtime(speech.start_time).strftime("%H")
                    temp_dic["end_time"] = timezone.localtime(speech.end_time).strftime("%H:%M")
                    temp_dic["color"] = speech.speech.topic.color
                    temp_dic["time"] = speech.speech.speech_type.time
                    temp_dic["is_speech"] = "true"
                    temp_dic["activity_pk"] = speech.speech.pk
                    temp_dic["title"] = speech.speech.title
                    temp_dic["room_name"] = speech.room.name
                    temp_dic["speech_pk"] = speech.speech.pk
                    temp_dic["speech_type"] = speech.speech.speech_type.pk
                    temp_dic['speech_topic'] = speech.speech.topic.pk
                    temp_dic["desc"] = "none"
                    temp_dic["is_scheduled"] = speech.speech.is_scheduled
                    activities_dic["1-" + str(speech.speech.pk)] = temp_dic
                else:
                    temp_dic["start_datetime"] = timezone.localtime(obj.start_time).strftime("%Y-%m-%d %H:%M:%S")
                    temp_dic["end_datetime"] = timezone.localtime(obj.end_time).strftime("%Y-%m-%d %H:%M:%S")
                    temp_dic["start_time"] = timezone.localtime(obj.start_time).strftime("%H:%M")
                    temp_dic["start_hour"] = timezone.localtime(obj.start_time).strftime("%H")
                    temp_dic["end_time"] = timezone.localtime(obj.end_time).strftime("%H:%M")
                    temp_dic["color"] = SPECIAL_ACTIVITY_COLOR
                    temp_dic["time"] = speech.special.type.time
                    temp_dic["activity_pk"] = speech.special.pk
                    temp_dic["desc"] = obj.text
                    temp_dic["is_speech"] = ""
                    temp_dic["is_scheduled"] = speech.special.is_scheduled
                    activities_dic["0-" + str(speech.special.pk)] = temp_dic
    return activities_dic


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'display'
        return context


def edit_agenda(request):
    return render(request, 'proposal/edit_agenda.html')


@method_decorator(login_required, name='dispatch')
class EditCharlas(PermissionRequiredMixin, CharlaContext, ListView):
    model = BlockSchedule
    order_by = "start_time"
    permission_required = 'proposal.add_blockschedule'

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            messages.success(
                self.request, _("Sorry, we need an event to display the schedule"))
            return redirect('sineventos/')
        return super(EditCharlas, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view'] = 'edit'
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('form_id'):
                if request.POST['form_id'] == 'delete':
                    block = BlockSchedule.objects.filter(id=request.POST['block']).first()
                    schedule = SpeechSchedule.objects.filter(start_time=block.start_time,
                                                             room=request.POST['room']).first()
                    if block.is_speech:
                        speech = schedule.speech
                        speech.is_scheduled = False
                        speech.save()
                    else:
                        special = schedule.special
                        special.is_scheduled = False
                        special.save()

                    block.delete()
                    schedule.delete()

            form = scheduleForm(request.POST)
            if request.POST.get('agenda'):
                result = json.loads(request.POST['agenda'])
                start_date = timezone.datetime.strptime(result[0]['start_time'], "%Y-%m-%d %H:%M:%S")
                start_date = timezone.datetime(hour=0, minute=0, day=start_date.day, month=start_date.month,
                                               year=start_date.year)
                end_date = timezone.datetime(hour=23, minute=59, day=start_date.day, month=start_date.month,
                                             year=start_date.year)

                block = BlockSchedule.objects.filter(start_time__gte=start_date, end_time__lte=end_date,
                                                     room=result[0]['room'])
                schedule = SpeechSchedule.objects.filter(start_time__gte=start_date, end_time__lte=end_date,
                                                         room=result[0]['room'])

                for speech in schedule:
                    if speech.speech:
                        speech.speech.is_scheduled = False
                        speech.speech.save()
                        if result[0].get('type'):
                            speech_type = SpeechType.objects.filter(id=int(result[0]['type'])).first()
                            speech.speech.speech_type = speech_type
                            speech.speech.save()

                block.delete()
                schedule.delete()

                for activities in result:
                    blockValid = False
                    scheduleValid = False

                    if activities['is_speech']:
                        speechSchedule = SpeechSchedule(start_time=timezone.datetime.strptime(activities['start_time'],
                                                                                              "%Y-%m-%d %H:%M:%S"),
                                                        end_time=timezone.datetime.strptime(
                                                            activities['end_time'], "%Y-%m-%d %H:%M:%S"),
                                                        speech=Speech.objects.filter(
                                                            id=int(activities['activity_pk'])).first(),
                                                        room=Room.objects.filter(id=int(activities['room'])).first(), )
                    else:
                        speechSchedule = SpeechSchedule(start_time=timezone.datetime.strptime(activities['start_time'],
                                                                                              "%Y-%m-%d %H:%M:%S"),
                                                        end_time=timezone.datetime.strptime(
                                                            activities['end_time'], "%Y-%m-%d %H:%M:%S"),
                                                        special=SpecialActivity.objects.filter(
                                                            id=int(activities['activity_pk'])).first(),
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
                        if activities.get('type'):
                            speech = Speech.objects.filter(id=int(activities['activity_pk'])).first()
                            speech.speech_type = SpeechType.objects.filter(id=int(activities['type'])).first()
                            speech.save()
                        speech = Speech.objects.filter(id=int(activities['activity_pk'])).first()
                        speech.is_scheduled = True
                        speech.save()

                    if not activities['is_speech'] and blockValid and scheduleValid:
                        special = SpecialActivity.objects.filter(id=int(activities['activity_pk'])).first()
                        special.is_scheduled = True
                        special.save()

            return redirect(reverse('edit_charlas'))


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
