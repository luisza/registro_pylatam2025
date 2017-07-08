'''
Created on 2 jun. 2017

@author: luis
'''
from django import forms
from ecsl.models import Inscription, Payment, PaymentOption
from django.utils.translation import ugettext_lazy as _


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

    field_order = [
        'first_name', 'last_name',
        'identification', 'nationality', 'other_nationality',
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
        exclude = ['user', 'status']


class PaymentForm(forms.ModelForm):
    option = forms.ModelChoiceField(widget=forms.RadioSelect,
                                    queryset=PaymentOption.objects.all().exclude(name="Beca"),
                                    label="Opción de pago",
                                    empty_label=None)

    class Meta:
        model = Payment
        fields = '__all__'
        exclude = ['user', 'confirmado']
