from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from ecsl.models import EventECSL
from proposal.forms import SpecialActivityForm
from proposal.models import SpecialActivity


@method_decorator(login_required, name='dispatch')
class CreateSpecialActivity(PermissionRequiredMixin, generic.CreateView):
    model = SpecialActivity
    form_class = SpecialActivityForm
    success_url = reverse_lazy('edit_charlas')
    permission_required = 'proposal.add_specialactivity'

    def form_valid(self, form):
        event = EventECSL.objects.filter(current=True).first()
        if not event:
            raise Http404
        form.instance.event = event
        return super(CreateSpecialActivity, self).form_valid(form)

