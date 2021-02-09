import hashlib
import random
import urllib

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from ecsl.models import Inscription, Payment, Becas, EventECSL, Package, PaymentOption
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from ecsl.forms import ProfileForm, PaymentForm, ContactForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from captcha.fields import CaptchaField
from django.core.mail import EmailMessage, send_mail
from django.core.mail import send_mail
from django.db.models import Count, Q


def noEvents(request):
    current_event = EventECSL.objects.filter(current=True).first()
    if current_event:
        return redirect('index')
    return render(request, 'no_events.html')


class Index(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            return redirect('no-events')
        return super(Index, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        proposal = None
        current_event = EventECSL.objects.filter(current=True).first()

        context = TemplateView.get_context_data(self, **kwargs)
        if self.request.user.is_authenticated:
            try:
                proposal = self.request.user.speech_set.count()
                if proposal > 0:
                    proposal = True
                else:
                    proposal = False
            except Exception as e:
                pass
            beca = Becas.objects.filter(user=self.request.user, event=current_event).first()
            if beca:
                context['becas_period'] = True
                context['beca'] = reverse_lazy('becas-detail')
            else:
                context['becas_period'] = current_event.is_beca_active
                context['beca'] = reverse_lazy('becas-create')
            if proposal:
                context['speech_url'] = proposal

        context['numparticipantes'] = Payment.objects.filter(event=current_event).count()
        context['genero'] = {
            'masculino': Payment.objects.filter(user__inscription__gender='Masculino', event=current_event).count(),
            'femenino': Payment.objects.filter(user__inscription__gender='Femenino', event=current_event).count(),
            'otro': Payment.objects.filter(user__inscription__gender='Otro', event=current_event).count(),
        }

        parms = {
            'panama': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Panamá')),
            'costarica': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Costa Rica')),
            'nicaragua': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Nicaragua')),
            'elsalvador': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='El Salvador')),
            'guatemala': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Guatemala')),
            'honduras': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Honduras')),
            'belize': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Belize')),
            'otro': Count('user__inscription__nationality', filter=Q(user__inscription__nationality='Otro')),
        }

        context['pais'] = Payment.objects.filter(event=current_event).aggregate(**parms)

        if current_event.checking_period:
            context['period'] = current_event.checking_period
        elif proposal:
            context['period'] = True
        context['event_name'] = str(current_event)
        context['event_logo'] = current_event.logo
        date = _("from %(start)s to %(end)s") % {'start': current_event.start_date.strftime("%B %-d"),
                                                 'end': current_event.end_date.strftime("%B %-d, %Y")}
        context['event_dates'] = date
        context['event_location'] = current_event.location
        context['event_description'] = current_event.description

        return context


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

