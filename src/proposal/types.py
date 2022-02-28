from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from ecsl.models import EventECSL
from proposal.forms import TypeForm
from proposal.models import SpeechType


@method_decorator(login_required, name='dispatch')
class CreateType(generic.CreateView):
    model = SpeechType
    form_class = TypeForm
    # permission_required = 'proposal.add_speechtype'

    def form_valid(self, form):
        event_id = self.request.POST.get('event_id')
        new_type = SpeechType.objects.create(
            name=form.cleaned_data['name'],
            time=form.data['eventTime'],
            event=EventECSL.objects.filter(current=True).first(),
            # que pasa si tengo 2 current True, pueden haber varios current
            # dentro del form mando el id del build agenda.
        )
        instance = {
            "type_name": new_type.name,
            "type_color": new_type.color,
            "type_event": new_type.event,
        }
        return JsonResponse(instance)

    def form_invalid(self, form):
        return JsonResponse("Ocurrio un error al guardar su tipo, intentelo de nuevo", status=400)