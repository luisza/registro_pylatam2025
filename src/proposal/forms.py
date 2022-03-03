from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Speech, Topic, SpeechType, SpecialActivity, Room


class SpeechForm(forms.ModelForm):
    speech_type = forms.ModelChoiceField(queryset=SpeechType.objects.filter(is_special=False), label=_("Type"))

    class Meta:
        model = Speech
        exclude = ('user', 'event', 'is_scheduled', 'speech_time_asked')


class TopicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].widget.input_type='color'

    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {
            'event': forms.HiddenInput,
            'color': forms.TextInput(attrs={'class': "form-control form-control-color"})
        }


class TypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].widget.input_type = 'range'

    class Meta:
        model = SpeechType
        fields = '__all__'
        widgets = {
            'event': forms.HiddenInput,
            'time': forms.TextInput(attrs={'step': "10", 'min': "10", 'max': "480"})
        }


class SpecialActivityForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=SpeechType.objects.filter(is_special=True), label=_("Type"))

    class Meta:
        model = SpecialActivity
        exclude = ('event', 'is_scheduled', 'room')


class RoomsCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('event',)
