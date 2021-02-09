from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from proposal.forms import TypeForm
from proposal.models import SpeechType

# @method_decorator(login_required, name='dispatch')
class CreateType(generic.CreateView):
    model = SpeechType
    form_class = TypeForm
    success_url = reverse_lazy('edit_charlas')
    # permission_required = 'proposal.add_speechtype'

    def form_invalid(self, form):
        return redirect(reverse_lazy('edit_charlas'))