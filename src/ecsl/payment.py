import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from ecsl.models import Inscription, Payment, Becas, EventECSL, Package, PaymentOption
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from ecsl.forms import ProfileForm, PaymentForm, ContactForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


@login_required
def payment_view(request):
    try:
        profile = Payment.objects.get(user=request.user)
        return redirect(reverse('edit_payment', args=(profile.pk,)))
    except:
        return redirect(reverse('create_payment'))

@method_decorator(login_required, name='dispatch')
class PaymentUpdate(UpdateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        current_event = EventECSL.objects.filter(current=True).first()
        if not current_event:
            messages.success(
                self.request, _("Sorry, there is no event for you to register"))
            return redirect('no-events')
        self.payment = get_object_or_404(Payment, pk=kwargs['pk'],
                                         user=request.user)
        return UpdateView.dispatch(self, request, *args, **kwargs)

    def form_valid(self, form):
        current_event = EventECSL.objects.filter(current=True).first()
        alreadyPaid = Payment.objects.filter(user=self.request.user, event=current_event).first()

        if alreadyPaid and alreadyPaid.confirmado == True and alreadyPaid.option.name == 'Paypal':
            messages.success(
                self.request, _("There was no transaction, you already paid for this event"))
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
    invoice = f"{request.user} -ECSL- {current_event.start_date.year} - {number}"
    item = 'ECSL-' + str(current_event.start_date.year) + str(inscription.id)
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

    if alreadyPaid and alreadyPaid.confirmado == True:
        messages.success(
            request, _("There was no transaction, you already paid for this event"))
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

        if alreadyPaid and alreadyPaid.confirmado == False and alreadyPaid.option.name == 'Paypal':
            alreadyPaid.delete()

        p_Option = PaymentOption.objects.filter(name='Paypal').first()
        payment = Payment(user=request.user, confirmado=False, event=current_event, option=p_Option, package=price)
        payment.save()
        form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'ecsl/process_payment.html', {'order': order, 'form': form, 'price': price})


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