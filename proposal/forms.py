from .models import Speech
from django import forms

class SpeechForm(forms.ModelForm):

    class Meta:
        model = Speech
        exclude = ('user', 'event')