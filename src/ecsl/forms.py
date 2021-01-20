'''
Created on 2 jun. 2017

@author: luis
'''
from django import forms
from ecsl.models import Inscription, Payment, PaymentOption, EventECSL
from proposal.models import SpeechSchedule, Topic, Speech, Register_Speech, \
    BlockSchedule
from django.utils.translation import ugettext_lazy as _

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

    field_order = [
        'first_name', 'last_name',
        'identification',
        'direccion_en_su_pais',
        'nationality', 'other_nationality',
        'gender', 'camiseta',
        'born_date', 'institution',
        'encuentros',
        'alimentary_restriction', 'health_consideration',
        'gustos_manias', 'observacion_gustos_manias',
        'comentario_general',
        'hora_de_llegada', 'hora_de_salida', 'medio_de_transporte',
        'lugar_de_arribo', 'observaciones_del_viaje', 'aparecer_en_participantes'
    ]

    def __init__(self, *args, **kwargs):
        self.user = None
        if 'instance' in kwargs and kwargs['instance']:
            self.user = kwargs['instance'].user

        if 'request' in kwargs:
            request = kwargs.pop('request')
            self.user = request.user
        if self.user:
            kwargs['initial']['first_name'] = self.user.first_name
            kwargs['initial']['last_name'] = self.user.last_name

        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        dev = super(ProfileForm, self).save(commit=commit)
        user = None
        if self.instance:
            user = self.instance.user
        elif self.user:
            user = self.user
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        return dev

    class Meta:
        model = Inscription
        fields = '__all__'
        exclude = ['user', 'status', 'event']


class PaymentForm(forms.ModelForm):
    option = forms.ModelChoiceField(widget=forms.RadioSelect,
                                    queryset=PaymentOption.objects.all().exclude(name="Beca").exclude(name="Paypal"),
                                    label="Opción de pago",
                                    empty_label=None)

    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['user', 'confirmado', 'event']


class ContactForm(forms.Form):

    Name = forms.CharField(
        label=False,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Name'),
                'class': 'form-control',
            }
        )
    )

    Email = forms.CharField(
        label=False,
        min_length=6,
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Email'),
                'class': 'form-control',
            }
        )
    )

    Subject = forms.CharField(
        label=False,
        min_length=2,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Subject'),
                'class': 'form-control',
            }
        )
    )

    Message = forms.CharField(
        label=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Message'),
                'class': 'form-control',
            }
        )
    )

class scheduleForm(forms.ModelForm):
    is_speech = forms.BooleanField()
    text = forms.CharField(max_length=250)
    color = forms.CharField(max_length=10)
    class Meta:
        model= SpeechSchedule
        fields= '__all__'