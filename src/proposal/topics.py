from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from ecsl.models import EventECSL
from proposal.forms import TopicForm
from proposal.models import Topic


@method_decorator(login_required, name='dispatch')
class CreateTopic(generic.CreateView):
    model = Topic
    form_class = TopicForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save()

        data = {
            "pk": instance.pk,
            "name": instance.name,
            "color": instance.color,
            "event": instance.event_id,
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)