from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from ecsl.models import Inscription, Payment, Becas
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from ecsl.forms import ProfileForm, PaymentForm
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

from cruds_adminlte.crud import UserCRUDView

class Index(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
                
        context = TemplateView.get_context_data(self, **kwargs)
        if self.request.user.is_authenticated():
            proposal=None
            try:
                proposal = self.request.user.speech_set.count()
                if proposal > 0:
                    proposal = reverse("speech:proposal_speech_list")
            except Exception as e:
                print(e)

            beca = Becas.objects.filter(user=self.request.user).first()
            if beca:
                context['beca'] = reverse('ecsl_becas_detail', kwargs={'pk': beca.pk})
            else:
                context['beca'] =reverse( 'ecsl_becas_create')
            if proposal:
                context['speech_url'] = proposal

        return context

@method_decorator(login_required, name='dispatch')
class CreateProfile(CreateView):
    model = Inscription
    form_class = ProfileForm

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, _('Profile created successfully, please register in the event'))
        form.instance.user = self.request.user
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
            error=True
            
        if error or not inscription:
            messages.success(self.request, "Lo lamentamos, primero actualiza tus datos y luego procede con el registro")
            return redirect(reverse('index'))
        
        if Payment.objects.all().count() >  settings.MAX_INSCRIPTION:
            messages.warning(self.request, "Lo lamentamos, ya no hay más espacio disponible")
            return redirect(reverse('index'))        
        return CreateView.dispatch(self, request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Felicidades su registro se ha completado satisfactoriamente, por favor registrese en las charlas")
        form.instance.user = self.request.user
        response= super(CreateRegister, self).form_valid(form)
        send_mail('Nuevo pago de inscripción',
            'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s'%(
                self.object.user.get_full_name(),
                self.object.option,
                self.object.codigo_de_referencia
                ),
            'not-reply@ecsl2017.softwarelibre.ca',
            [self.object.option.email],
             fail_silently=False
            )
        
        inscription = self.object.user.inscription
        inscription.status=2
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
        messages.success(self.request, _('Register updated successfully'))
        response = UpdateView.form_valid(self, form)
        send_mail('Cambio en la suscripción de %s'%(self.object.user.get_full_name(),),
            'Hola, %s ha pagado la inscripción con la opción %s y el código de identificación %s'%(
                self.object.user.get_full_name(),
                self.object.option,
                self.object.codigo_de_referencia
                ),
            'not-reply@ecsl2017.softwarelibre.ca',
            [self.object.option.email],
             fail_silently=False
            )       
        return response
    
    
class BecasCRUD(UserCRUDView):
    model = Becas
    check_perms = False
    views_available=['create', 'detail']
    fields = [
        'razon', 'aportes_a_la_comunidad', 'tiempo' , 'observaciones'
        ]
    
    def get_create_view(self):
        Cview = super(BecasCRUD, self).get_create_view()
        class BecaCreate(Cview):
            def dispatch(self, request, *args, **kwargs):
                error = False
                try:
                    inscription = request.user.inscription
                except:
                    error=True
                    
                if error or not inscription:
                    messages.success(self.request, "Lo lamentamos, primero actualiza tus datos y luego procede con el registro")
                    return redirect(reverse('index'))
                
                beca = Becas.objects.filter(user=request.user).first()
                if beca:
                    return redirect("ecsl_becas_detail", pk=beca.pk )
                return super(BecaCreate, self).dispatch(request, *args, **kwargs)   
            
            def get_success_url(self):
                messages.success(self.request, "Hemos recibido su solicitud de beca satisfactoriamente")
                return reverse('index')                 
        return BecaCreate
                

    
becas = BecasCRUD().get_urls()