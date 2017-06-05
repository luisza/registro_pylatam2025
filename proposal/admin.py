from django.contrib import admin

# Register your models here.

from proposal.models import SpeechType, Topic, Speech


class SpeechAdmin(admin.ModelAdmin):
    list_display = ['speaker_name', 'title', 'skill_level', 'speaker_registered']
    list_filter = ['topic', 'speech_type']

admin.site.register(Speech, SpeechAdmin)
admin.site.register([SpeechType, Topic])
