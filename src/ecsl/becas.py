import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from ecsl.models import Inscription, Payment, Becas, EventECSL, Package, PaymentOption
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@method_decorator(login_required, name='dispatch')
class BecasCreate(CreateView):
    model = Becas
    fields = [
        'razon', 'aportes_a_la_comunidad', 'tiempo', 'observaciones'
    ]

    def form_valid(self, form):
        beca = form.save(commit=False)
        beca.user = self.request.user
        beca.event = EventECSL.objects.filter(current=True).first()
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

        event = EventECSL.objects.filter(current=True).first()
        beca = Becas.objects.filter(user=request.user, event=event).first()
        if beca:
            return redirect("becas-detail", pk=beca.pk)

        if not event.is_beca_active:
            if not event.beca_start or not event.beca_end:
                messages.success(
                    request, _("Sorry, but the scholarship application period has not been established yet. "
                               "We will let you know via email when this occurs."))
            else:
                messages.success(
                    request, _("Sorry, but the scholarship application period is not available at the time. "
                           "Application period: %(start)s - %(end)s") % {
                             'start': event.beca_start.strftime("%b %-d, %Y")
                             , 'end': event.beca_end.strftime("%b %-d, %Y")})
            return redirect(reverse_lazy('index'))

        return super(BecasCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(
            self.request, _("We have received your scholarship application successfully"))
        return reverse_lazy('index')


@method_decorator(login_required, name='dispatch')
class BecasDetail(DetailView):
    model = Becas
    fields = [
        'estado', 'razon', 'aportes_a_la_comunidad', 'tiempo', 'observaciones'
    ]

    def dispatch(self, request, *args, **kwargs):
        event = EventECSL.objects.filter(current=True).first()
        beca = Becas.objects.filter(pk=kwargs['pk'], event=event).first()
        if not beca or beca.user.id != request.user.id:
            messages.success(
                request, _("Sorry, but the scholarship application you are looking for does not exist"))
            return redirect(reverse_lazy('index'))
        return super(BecasDetail, self).dispatch(request, *args, **kwargs)