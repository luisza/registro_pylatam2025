from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SpeechForm, TopicForm, TypeForm, SpecialActivityForm, RoomsCreateForm
from django.urls import reverse, reverse_lazy
from proposal.models import Speech, Room, SpeechSchedule
from ecsl.models import Payment, Inscription, EventECSL
import hashlib
import urllib
from django.http.response import HttpResponseRedirect
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
from .models import Topic, SpeechType, SpecialActivity


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
        return JsonResponse(data={'result': result, 'color': colors, 'times': times, 'types': types,})


def get_participants(request):
    dev = []
    default = "https://ecsl2017.softwarelibre.ca/wp-content/uploads/2017/01/cropped-photo_2017-01-30_20-55-06.jpg".encode(
        'utf-8')
    size = 50
    for payment in Payment.objects.all().order_by('?'):
        email = payment.user.email.lower().encode('utf-8')

        insc = Inscription.objects.filter(user=payment.user).first()
        if insc and insc.aparecer_en_participantes:
            name = payment.user.get_full_name()

            url = "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(
                email).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))

            dev.append({'url': url, 'name': name})

    return JsonResponse(dev, safe=False)


class CreateRoom(generic.CreateView):
    model = Room
    form_class = RoomsCreateForm
    success_url = reverse_lazy('list_charlas')

    def form_valid(self, form):
        form.instance.event = EventECSL.objects.filter(current=True).first()
        response = super(CreateRoom, self).form_valid(form)
        return response


class CreateTopic(generic.CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy('list_charlas')


class CreateType(generic.CreateView):
    model = SpeechType
    form_class = TypeForm
    success_url = reverse_lazy('list_charlas')


class CreateSpecialActivity(generic.CreateView):
    model = SpecialActivity
    form_class = SpecialActivityForm
    success_url = reverse_lazy('list_charlas')

    def form_valid(self, form):
        event = EventECSL.objects.filter(current=True).first()
        if event:
            form.instance.event = event
            response = super(CreateSpecialActivity, self).form_valid(form)
        return response


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