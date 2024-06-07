from django import template
from ecsl.models import EventECSL

register = template.Library()


@register.simple_tag
def phone():
    phone = ''
    event = EventECSL.objects.filter(current=True).first()
    if event:
        phone = event.phone_event
    return phone

@register.simple_tag
def location():
    location = ''
    event = EventECSL.objects.filter(current=True).first()
    if event:
        location = event.location
    return location
