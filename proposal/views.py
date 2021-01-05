from django.shortcuts import render

# Create your views here.
from django.views import generic

from proposal.models import Speech
# from cruds_adminlte.crud import UserCRUDView
from ecsl.models import Payment, Inscription
import hashlib
import urllib
from django.http.response import JsonResponse


# class ProposalSpeech:
#     model = Speech
#     namespace = "speech"
#     check_perms = False
#     views_available = ['list', 'update', 'detail']
#     list_fields = ['title', 'topic',  'skill_level']
#     fields = [
#         'speaker_information',
#         'title',
#         'topic',
#         'description',
#         'audience',
#         'skill_level',
#         'notes',
#         'speech_type',
#         'presentacion']

class ProposalSpeech(generic.ListView):
    model = Speech
    namespace = "speech"


proposals = ProposalSpeech()


def get_participants(request):
    dev = []
    default = "https://ecsl2017.softwarelibre.ca/wp-content/uploads/2017/01/cropped-photo_2017-01-30_20-55-06.jpg".encode(
        'utf-8')
    size = 50
    for payment in Payment.objects.all().order_by('?'):
        email = payment.user.email.lower().encode('utf-8')

        insc = Inscription.objects.filter(user=payment.user).first()
        if insc and insc.aparecer_en_participantes:
            name = payment.user.get_full_name()

            url = "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(
                email).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))

            dev.append({'url': url, 'name': name})

    return JsonResponse(dev, safe=False)
