from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SpeechForm
from django.urls import reverse, reverse_lazy
from proposal.models import Speech
from ecsl.models import Payment, Inscription, EventECSL
import hashlib
import urllib
from django.http.response import JsonResponse, HttpResponseRedirect
from django.views import generic
from django.utils.translation import ugettext_lazy as _


# Create your views here.


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
        return Speech.objects.filter(user=self.request.user)


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
