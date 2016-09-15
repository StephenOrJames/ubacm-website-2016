from django.views.generic.list import ListView

from .models import Event


class EventsList(ListView):
    model = Event
    template_name = 'events.html'
