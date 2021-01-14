import random

from django.http import HttpResponseRedirect
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
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import date as _date

from django.core.mail import send_mail
# Create your views here.


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
        else:
            return super(Index, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()

        context = TemplateView.get_context_data(self, **kwargs)
        if self.request.user.is_authenticated:
            proposal = None
            try:
                proposal = self.request.user.speech_set.count()
                if proposal > 0:
                    proposal = reverse("speech:proposal_speech_list")
            except Exception as e:
                pass
            beca = Becas.objects.filter(user=self.request.user).first()
            if beca:
                context['beca'] = reverse_lazy('becas-detail')
            else:
                context['beca'] = reverse_lazy('becas-create')
            if proposal:
                context['speech_url'] = proposal

        context['numparticipantes'] = Payment.objects.all().count()
        context['genero'] = {
            'masculino': Payment.objects.filter(user__inscription__gender='Masculino').count(),
            'femenino': Payment.objects.filter(user__inscription__gender='Femenino').count(),
            'otro': Payment.objects.filter(user__inscription__gender='Otro').count(),
        }

        context['pais'] = {

            'panama': Payment.objects.filter(user__inscription__nationality='Panamá').count(),
            'costarica': Payment.objects.filter(user__inscription__nationality='Costa Rica').count(),
            'nicaragua': Payment.objects.filter(user__inscription__nationality='Nicaragua').count(),
            'elsalvador': Payment.objects.filter(user__inscription__nationality='El Salvador').count(),
            'guatemala': Payment.objects.filter(user__inscription__nationality='Guatemala').count(),
            'honduras': Payment.objects.filter(user__inscription__nationality='Honduras').count(),
            'belize': Payment.objects.filter(user__inscription__nationality='Belize').count(),
            'otro': Payment.objects.filter(user__inscription__nationality='Otro').count(),

        }

        context['event_name'] = str(current_event)
        context['event_logo'] = current_event.logo
        date = _("from %(start)s to %(end)s")%{'start': current_event.start_date.strftime("%B %-d"),'end': current_event.end_date.strftime("%B %-d, %Y")}
        context['event_dates'] = date
        context['event_location'] = current_event.location
        context['event_description'] = current_event.description

        return context


@method_decorator(login_required, name='dispatch')
class CreateProfile(CreateView):
    model = Inscription
    form_class = ProfileForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        event = EventECSL.objects.filter(current=True).first()
        messages.success(self.request, _(
            'Profile created successfully, please register in the event'))
        form.instance.user = self.request.user
        form.instance.event = event
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super(CreateProfile, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        profile = self.model.objects.filter(user=request.user).first()
        if profile:
            return redirect(reverse('edit_profile', args=(profile.pk,)))
        return super(CreateProfile, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = self.model.objects.filter(user=request.user).first()
        if profile:
            return redirect(reverse('edit_profile', args=(profile.pk,)))
        return CreateView.post(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        context = CreateView.get_form_kwargs(self)
        context['request'] = self.request
        return context


@method_decorator(login_required, name='dispatch')
class UpdateProfile(UpdateView):
    model = Inscription
    form_class = ProfileForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        self.inscription = get_object_or_404(Inscription, pk=kwargs['pk'],
                                             user=request.user)
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully'))
        return UpdateView.form_valid(self, form)


@login_required
def profile_view(request):
    try:
        profile = Inscription.objects.get(user=request.user)
        return redirect(reverse('edit_profile', args=(profile.pk,)))
    except:
        return redirect(reverse('create_profile'))


@login_required
def payment_view(request):
    try:
        profile = Payment.objects.get(user=request.user)
        return redirect(reverse('edit_payment', args=(profile.pk,)))
    except:
        return redirect(reverse('create_payment'))


@method_decorator(login_required, name='dispatch')
class CreateRegister(CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        error = False
        try:
            inscription = request.user.inscription
        except:
            error = True

        if error or not inscription:
            messages.success(
                self.request, _("Sorry, first you have to update your data and then proceed with the registration"))
            return redirect(reverse('index'))


        if Payment.objects.all().count() > settings.MAX_INSCRIPTION:
            messages.warning(
                self.request, _("Sorry, there are no more spaces available"))
            return redirect(reverse('index'))

        return CreateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            _("Congratulations, your registration has been completed successfully, please enroll into the speeches"))
        form.instance.user = self.request.user
        form.instance.event = EventECSL.objects.filter(current=True).first()

        response = super(CreateRegister, self).form_valid(form)
        send_mail('Nuevo pago de inscripción',
                  'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s' % (
                      self.object.user.get_full_name(),
                      self.object.option,
                      self.object.codigo_de_referencia
                  ),
                  'not-reply@ecsl2017.softwarelibre.ca',
                  [self.object.option.email],
                  fail_silently=False
                  )

        inscription = self.object.user.inscription
        inscription.status = 2
        inscription.save()
        return response


@method_decorator(login_required, name='dispatch')
class PaymentUpdate(UpdateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        self.payment = get_object_or_404(Payment, pk=kwargs['pk'],
                                         user=request.user)
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        current_event = EventECSL.objects.filter(current=True).first()
        alreadyPaid = Payment.objects.filter(user=self.request.user, event=current_event).first()

        if alreadyPaid and alreadyPaid.confirmado==True and alreadyPaid.option.name == 'Paypal':
            messages.success(
                self.request, _("No action, you already paid for this event"))
            return redirect(reverse_lazy('index'))

        messages.success(self.request, _('Register updated successfully'))
        response = UpdateView.form_valid(self, form)
        send_mail('Cambio en la suscripción de %s' % (self.object.user.get_full_name(),),
                  'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s' % (
                      self.object.user.get_full_name(),
                      self.object.option,
                      self.object.codigo_de_referencia
                  ),
                  'not-reply@ecsl2017.softwarelibre.ca',
                  [self.object.option.email],
                  fail_silently=False
                  )
        return response


def contactUs(request):
    form = ContactForm()

    if request.user.is_authenticated:
        form.fields['Name'].initial = request.user.username
        form.fields['Email'].initial = request.user.email
    context = {
        'form': form,
    }

    return render(request, 'contact/contact_us.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            if (send_mail(form.cleaned_data.get("Subject"),
                       'Nombre:' + form.cleaned_data.get('Name') + '\n' + form.cleaned_data.get("Message"),
                       form.cleaned_data.get("Email"),
                       ['not-reply@ecsl2017.softwarelibre.ca'],
                       fail_silently=False
                       )):
                messages.success(request, _('Thank! Your message was sent successfully'))
    return redirect(reverse('contact-us'))


def process_payment(request, text):
    order = ''
    host = request.get_host()
    inscription = request.user.inscription
    price = Package.objects.filter(name=text).first()

    if not price:
        messages.success(
            request, _("Invalid Package"))
        return redirect(reverse_lazy('index'))

    current_event = EventECSL.objects.filter(current=True).first()
    number = random.randint(1000, 9999)
    invoice= str(request.user) + '-ECSL-' + str(current_event.start_date.year) + str(number)
    item ='ECSL-' + str(current_event.start_date.year) + str(inscription.id)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': price.price,
        'item_name': item,
        'invoice': invoice,
        'currency_code': 'USD',
        'notify_url': 'https//{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'https//{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    alreadyPaid = Payment.objects.filter(user=request.user, event=current_event).first()


    if alreadyPaid and alreadyPaid.confirmado==True:
        messages.success(
            request, _("No action, you already paid for this event"))
        return redirect(reverse_lazy('index'))
    else:

        if price.price <= 0.00:
            if alreadyPaid and alreadyPaid.confirmado == False and alreadyPaid.option.name == 'Paypal':
                alreadyPaid.delete()
            p_Option = PaymentOption.objects.filter(name='Paypal').first()
            payment = Payment(user=request.user, confirmado=True, event=current_event, option=p_Option, package=price)
            payment.save()
            messages.success(
                request, _("You registration is complete, this package is free"))
            return redirect(reverse_lazy('index'))

        if alreadyPaid and alreadyPaid.confirmado==False and  alreadyPaid.option.name == 'Paypal':
            alreadyPaid.delete()

        p_Option = PaymentOption.objects.filter(name='Paypal').first()
        payment = Payment(user=request.user, confirmado=False, event=current_event, option=p_Option, package=price)
        payment.save()
        form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecsl/process_payment.html', {'order': order, 'form': form, 'price' : price})


@csrf_exempt
def payment_done(request):
    inscription = request.user.inscription
    inscription.status = 2
    inscription.save()

    payment = Payment.objects.filter(user=request.user).first()
    payment.confirmado = True
    payment.save()
    return render(request, 'ecsl/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecsl/payment_cancelled.html')


def checkout(request):
    return render(request, 'ecsl/checkout.html', locals())


class BecasCreate(CreateView):
    model = Becas
    fields = [
        'razon', 'aportes_a_la_comunidad', 'tiempo', 'observaciones'
    ]

    def form_valid(self, form):
        beca = form.save(commit=False)
        beca.user = self.request.user
        beca.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        error = False
        try:
            inscription = request.user.inscription
        except:
            error = True

        if error or not inscription:
            messages.success(
                self.request, _("Sorry, first you have to update your data and then proceed with the registration"))
            return redirect(reverse_lazy('index'))

        beca = Becas.objects.filter(user=request.user).first()
        if beca:
            return redirect("becas-detail", pk=beca.pk)
        return super(BecasCreate, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        messages.success(
            self.request, _("We have received your scholarship application successfully"))
        return reverse_lazy('index')


class BecasDetail(DetailView):
    model = Becas
    fields = [
       'estado', 'razon', 'aportes_a_la_comunidad', 'tiempo', 'observaciones'
    ]
