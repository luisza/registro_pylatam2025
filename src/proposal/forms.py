from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Speech, Topic, SpeechType, SpecialActivity, Room


class SpeechForm(forms.ModelForm):
    speech_type = forms.ModelChoiceField(queryset=SpeechType.objects.filter(is_special=False), label=_("Type"))

    class Meta:
        model = Speech
        exclude = ('user', 'event', 'is_scheduled', 'speech_time_asked')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('objects', 'event', 'color')


class TypeForm(forms.ModelForm):
    class Meta:
        model = SpeechType
        fields = '__all__'


class SpecialActivityForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=SpeechType.objects.filter(is_special=True), label=_("Type"))

    class Meta:
        model = SpecialActivity
        exclude = ('event', 'is_scheduled', 'room')


class RoomsCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ('event',)
