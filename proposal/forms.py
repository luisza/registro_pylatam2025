from .models import Speech
from django import forms

class SpeechForm(forms.ModelForm):

    class Meta:
        model = Speech
        fields = '__all__'
        exclude = ('user', 'event')

