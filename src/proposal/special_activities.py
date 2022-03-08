from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from ecsl.models import EventECSL
from proposal.forms import SpecialActivityForm
from proposal.models import SpecialActivity, SpeechType


@method_decorator(login_required, name='dispatch')
class CreateSpecialActivity(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'proposal.add_specialactivity'
    model = SpecialActivity
    form_class = SpecialActivityForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save()

        data = {
            "pk": instance.pk,
            "name": instance.name,
            "type": instance.type_id,
            "time": SpeechType.objects.get(id=instance.type_id).time,
            "message": instance.message,
            "event": instance.event_id,
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors)

