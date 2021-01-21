from .models import Speech, Topic, SpeechType, SpecialActivity
from django import forms

class SpeechForm(forms.ModelForm):

    class Meta:
        model = Speech
        exclude = ('user', 'event', 'time_given')

class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = '__all__'

class TypeForm(forms.ModelForm):

    class Meta:
        model = SpeechType
        fields = '__all__'

class SpecialActivityForm(forms.ModelForm):

    class Meta:
        model = SpecialActivity
        exclude = ('event',)
