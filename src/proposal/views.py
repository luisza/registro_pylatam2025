import json

from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Case, Value, When
from rest_framework.generics import ListCreateAPIView

from ecsl.models import EventECSL
from proposal.models import Speech, SpeechSchedule, SpecialActivity
from .forms import SpeechForm
from .models import SpeechType

# Create your views here.
from .serializers import SpeechScheduleSerializer


class SpeechListView(generic.ListView):
    template_name = 'proposal/speech_list.html'
    context_object_name = 'speech_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        event = EventECSL.objects.filter(current=True).first()
        context = generic.ListView.get_context_data(self, **kwargs)
        if event.checking_period:
            context['period'] = event.checking_period
        return context

    def dispatch(self, request, *args, **kwargs):
        proposal = None
        event = EventECSL.objects.filter(current=True).first()
        if not self.request.user.is_authenticated and event:
            messages.warning(
                self.request, _("We are sorry! You have to be registered as a system user to be able to send"
                                "a proposal speech"))
            return redirect(reverse_lazy('index'))
        elif not event:
            return redirect(reverse('index'))
        elif request.user.is_authenticated:
            try:
                proposal = request.user.speech_set.count()
                if proposal > 0:
                    proposal = True
                else:
                    proposal = None
            except Exception as e:
                pass
        if not event.checking_period and not proposal:
            messages.warning(
                self.request, _("We are sorry! The proposal speech period is not active"
                                ))
            return redirect(reverse('index'))
        return super(SpeechListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        event = EventECSL.objects.filter(current=True).first()
        if event:
            return Speech.objects.filter(user=self.request.user, event=event)


def get_color_speech(request, result):
    colors = None
    if result:
        colors = []
        for speech in result:
            colors.append(speech.topic.color)
    return colors


def get_times_speech(request, result):
    times = None
    if result:
        times = []
        for speech in result:
            times.append(speech.speech_type.time)
    return times


def get_all_speeches(request):
    if request.method == 'POST':
        result = []
        colors = []
        event = EventECSL.objects.filter(current=True).first()
        if event and 'topic' in request.POST and 'type' in request.POST:
            if request.POST['topic'] == 'None' and request.POST['type'] == 'None':
                result_query = Speech.objects.filter(event=event, is_scheduled=False)
                result = serializers.serialize('json', result_query)

            elif request.POST['topic'] == 'None' and request.POST['type'] != 'None':
                result_query = Speech.objects.filter(event=event, speech_type=request.POST['type'],
                                                     is_scheduled=False)
                result = serializers.serialize('json', result_query)

            elif request.POST['type'] == 'None' and request.POST['topic'] != 'None':
                result_query = Speech.objects.filter(event=event, topic=request.POST['topic'],
                                                     is_scheduled=False)
                result = serializers.serialize('json', result_query)
            else:
                result_query = Speech.objects.filter(event=event, speech_type=request.POST['type'],
                                                     is_scheduled=False, topic=request.POST['topic'])
                result = serializers.serialize('json', result_query)

            times = get_times_speech(request, result_query)
            colors = get_color_speech(request, result_query)
            types = SpeechType.objects.filter(is_special=False)
            types = serializers.serialize('json', types)
        return JsonResponse(data={'result': result, 'color': colors, 'times': times, 'types': types, })


def deleteView(request, speech_id):
    if request.method == 'POST':
        speech = Speech.objects.get(pk=speech_id)
        speech.delete()
    return HttpResponseRedirect(reverse('proposal:speech-list'))


def createUpdateview(request, speech_id=None):
    context = {}
    speech_form = SpeechForm()
    event = EventECSL.objects.get(current=True)
    proposal = None
    if not request.user.is_authenticated and event:
        messages.warning(
            request, _("We are sorry! You have to be registered as a system user to be able to send"
                       "a proposal speech"))
        return redirect(reverse_lazy('index'))
    elif not event:
        return redirect(reverse('index'))
    elif request.user.is_authenticated:
        if speech_id != None:
            if Speech.objects.filter(id=speech_id).first().user != request.user:
                return redirect(reverse_lazy('index'))
        try:
            proposal = request.user.speech_set.count()
            if proposal > 0:
                proposal = True
            else:
                proposal = None
        except Exception as e:
            pass
    if not event.checking_period and not proposal:
        messages.warning(
            request, _("We are sorry! The proposal speech period is not active"
                       ))
        return redirect(reverse('index'))
    if request.method == 'POST' and not speech_id:
        speech_form = SpeechForm(request.POST)
        if speech_form.is_valid():
            form = speech_form.save(commit=False)
            form.speech_time_asked = form.speech_type.time
            form.user = request.user
            form.event = event
            form.save()
    elif request.method == 'POST' and speech_id:
        speech = Speech.objects.filter(pk=speech_id).first()
        speech_form = SpeechForm(request.POST, instance=speech)
        if speech_form.is_valid():
            form = speech_form.save(commit=False)
            form.event = event
            form.save()
    elif speech_id and request.method == 'GET':
        speech = Speech.objects.filter(pk=speech_id).first()
        speech_form = SpeechForm(instance=speech)

    context['speech_form'] = speech_form

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('proposal:speech-list'))
    else:
        return render(request, "proposal/speech_form.html", context)


@require_http_methods(["POST"])
def removeSpeechScheduleFromCalendarView(request):
    try:
        data = json.loads(request.body)

        for i in range(len(data)):
            if data[str(i)]:
                speech_result = SpeechSchedule.objects.filter(html_id=data[str(i)]).first()
                if speech_result:
                    if speech_result.speech:
                        Speech.objects.filter(
                            pk=speech_result.speech.pk
                        ).update(
                            is_scheduled=Case(
                                When(is_scheduled=True, then=Value(False)),
                                default=Value(True)
                            )
                        )
                    if speech_result.special:
                        SpecialActivity.objects.filter(
                            pk=speech_result.special.pk
                        ).update(
                            is_scheduled=Case(
                                When(is_scheduled=True, then=Value(False)),
                                default=Value(True)
                            )
                        )
                    speech_result.delete()

        return HttpResponse('Events deleted', status=200)

    except Exception as e:
        return HttpResponse('Something went wrong', status=400)


class EventScheduleViewSet(viewsets.ModelViewSet):
    queryset = SpeechSchedule.objects.all()
    model = SpeechSchedule
    serializer_class = SpeechScheduleSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(data=self.request.data, many=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            for index, speech in enumerate(serializer.validated_data):
                obj, created = self.model.objects.update_or_create(
                    html_id=speech['html_id'],
                    defaults={
                        'start_time': speech['start_time'],
                        'end_time': speech['end_time'],
                        'speech': speech['speech'],
                        'special': speech['special'],
                        'room': speech['room']
                    },
                )
                if created:
                    if obj.speech:
                        Speech.objects.filter(
                            pk=obj.speech.pk
                        ).update(
                            is_scheduled=Case(
                                When(is_scheduled=True, then=Value(False)),
                                default=Value(True)
                            )
                        )
                    if obj.special:
                        SpecialActivity.objects.filter(
                            pk=obj.special.pk
                        ).update(
                            is_scheduled=Case(
                                When(is_scheduled=True, then=Value(False)),
                                default=Value(True)
                            )
                        )
                serializer.data[index].update({'id': obj.id, 'html_id': obj.html_id})
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

