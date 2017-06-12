from django.shortcuts import render

# Create your views here.


from proposal.models import Speech
from cruds_adminlte.crud import UserCRUDView

class ProposalSpeech(UserCRUDView):
    model = Speech
    namespace = "speech"
    check_perms = False
    views_available=['list', 'create','update', 'detail']
    list_fields = ['title','topic',  'skill_level']
    fields = [
        'speaker_information',
        'title',
        'topic',
        'description',
        'audience',
        'skill_level',
        'notes',
        'speech_type', 
        'presentacion']

proposals = ProposalSpeech()
