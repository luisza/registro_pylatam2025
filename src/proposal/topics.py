from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from proposal.forms import TopicForm
from proposal.models import Topic

class CreateTopic(generic.CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy('edit_charlas')

    def form_invalid(self, form):
        return redirect(reverse_lazy('edit_charlas'))