import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from events.models import Event
from main.models import ContactForm, EBoard, BackgroundImage


def index(request):
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    one_month_away = (datetime.date.today() + datetime.timedelta(days=62)).strftime("%Y-%m-%d")
    events = Event.objects.filter(date__range=[current_date, one_month_away]).order_by('-date').all()[:4]
    if len(events) < 4:
        events = Event.objects.order_by('-date').all()[:4]
    eboard = EBoard.objects.filter(id=len(EBoard.objects.all())).first()
    background = BackgroundImage.objects.all()[0]
    return render(request, 'index.html', {'home': True, 'eboard': eboard, 'events': events, 'background': background})


def contact(request):
    data = {
        'name': request.POST.get('name', ''),
        'email': request.POST.get('email', ''),
        'phone': request.POST.get('phone', ''),
        'message': request.POST.get('message', '')
    }
    wrong = False
    for key, value in data.items():
        if key != 'phone' and len(value) < 5:
            messages.error(request, "Your " + key + " was too short.")
            wrong = True
    if wrong:
        return redirect('index')

    contactform = ContactForm.objects.create(name=data['name'], email=data['email'], phone=data['phone'],
                                             message=data['message'])
    contactform.save()
    messages.success(request, "Your message was sent!")
    return redirect('index')
