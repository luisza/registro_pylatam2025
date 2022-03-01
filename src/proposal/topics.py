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

    def get_form(self):
        return self.form_class(self.request.POST)

    def form_valid(self, form):
        event_id = self.request.POST.get('event_id')
        new_topic = Topic.objects.create(
            name=form.cleaned_data['name'],
            color=form.data['colorPicker'],
            event=EventECSL.objects.filter(pk=event_id),
        )
        instance = {
            "topic_name": new_topic.name,
            "topic_color": new_topic.color,
            "topic_event": new_topic.event,
        }
        return JsonResponse(instance)

    def form_invalid(self, form):
        return JsonResponse("Ocurrio un error al guardar su tema, intentelo de nuevo", status=400)