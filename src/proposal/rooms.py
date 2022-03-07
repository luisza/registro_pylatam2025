from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from ecsl.models import EventECSL
from proposal.forms import RoomsCreateForm
from proposal.models import Room


@method_decorator(login_required, name='dispatch')
class CreateRoom(PermissionRequiredMixin, generic.CreateView):
    model = Room
    form_class = RoomsCreateForm
    permission_required = 'proposal.add_room'

    def form_valid(self, form):
        form.instance.event = EventECSL.objects.filter(current=True).first()
        self.success_url = reverse_lazy('edit_charlas', kwargs={'pk': form.instance.event.pk})
        response = super(CreateRoom, self).form_valid(form)
        return response
