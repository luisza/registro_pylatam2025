from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView

from ecsl.forms import ProfileForm, PaymentForm
from ecsl.models import Inscription, Payment, EventECSL


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


@method_decorator(login_required, name='dispatch')
class CreateRegister(CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            messages.success(
                self.request, _("Sorry, there is no event for you to register"))
            return redirect('no-events')
        error = False
        try:
            inscription = request.user.inscription
        except:
            error = True

        if error or not inscription:
            messages.success(
                self.request, _("Sorry, first you have to update your data and then proceed with the registration"))
            return redirect(reverse('index'))

        event = EventECSL.objects.filter(current=True).first()
        if Payment.objects.filter(event=event).count() >= event.max_inscription:
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
