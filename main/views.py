import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from contacts.models import Profile, Newsletter
from events.models import Event, Meeting, Response
from lib import random_generator
from lib.ubitscrap import get_name
from main.models import ContactForm, EBoard, BackgroundImage


def index(request):
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    one_month_away = (datetime.date.today() + datetime.timedelta(days=62)).strftime("%Y-%m-%d")
    events = Event.objects.filter(date__range=[current_date, one_month_away]).order_by('-date').all()[:4]
    if len(events) < 4:
        events = Event.objects.order_by('-date').all()[:4]
    eboard = EBoard.objects.filter(id=len(EBoard.objects.all())).first()
    background = BackgroundImage.objects.all()[0]
    return render(request, 'index.html',
                  {'home': True, 'eboard': eboard, 'events': events.reverse(), 'background': background})


def add_user(request):
    email = request.POST.get('email', '')
    if not email.endswith('@buffalo.edu'):
        messages.error(request, "Must be a UB email")
        return redirect('index')
    if len(email) < 14:
        messages.error(request, "Email is too short")
    if User.objects.filter(email=email).first():
        messages.error(request, "That email is already used")
        return redirect('index')
    ubit = str(email).split('@')[0]
    name_list = get_name(ubit)
    if None in name_list:
        messages.error(request, "That name was not found")
        return redirect('index')
    user = User.objects.create_user(ubit, email, random_generator(), first_name=name_list[0],
                                    last_name=name_list[1])
    user.save()
    profile = Profile.objects.create(attended=0, user=user, phone_number="00")
    profile.save()
    messages.success(request, "Successfully added you to the list!")
    return redirect('index')


@csrf_exempt
def add_user_rest(request):
    email = request.POST.get('email', '')
    if User.objects.filter(email=email).first():
        return JsonResponse({'data': 'Email already exists - ' + email})
    ubit = str(email).split('@')[0]
    try:
        name_list = get_name(ubit)
    except:
        name_list = ["Unknown", "Unknown"]
    if len(ubit) < 2 or ubit is None:
        return JsonResponse({'data': 'UBIT name is empty'})
    user = User.objects.create_user(ubit, email, random_generator(), first_name=name_list[0],
                                    last_name=name_list[1])
    user.save()
    profile = Profile.objects.create(attended=0, user=user, phone_number="00")
    profile.save()
    return JsonResponse({'data': 'Email added - ' + email})


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


def show_newsletter(request, letter_id=None):
    if letter_id is None:
        messages.error(request, "Web page not found.")
        return redirect('index')
    newsletter = Newsletter.objects.filter(id=int(letter_id)).first()
    if newsletter is None:
        messages.error(request, "Newsletter not found.")
        return redirect('index')
    return render(request, 'newsletter.html', {'widgets': newsletter.widgets.all(), 'newsletter': newsletter})


def unsubscribe_email(request, email=None):
    if email is None:
        messages.error(request, "Web page not found")
        return redirect('index')
    user = User.objects.filter(username=email).first()
    if user is None:
        messages.error(request, "Email not found in our servers")
        redirect('index')
    user.profile.send_email = False
    user.profile.save()
    user.save()
    messages.success(request, "Email successfully unsubscribed.")
    return redirect('index')


"""Meeting information"""


def show_meeting(request):
    from events.models import Meeting
    if len(Meeting.objects.all()) < 1:
        messages.error(request, "No meetings currently!")
        return redirect('index')
    meeting = Meeting.objects.all().reverse()[0]
    if meeting and meeting.is_open:
        return render(request, 'meeting.html', {'meeting': meeting})
    messages.error(request, "The meeting form isn't open yet!")
    return redirect('index')


def add_response(request):
    from events.models import Meeting
    from events.models import Response
    email = request.POST.get('name', '')
    meeting = Meeting.objects.all().reverse()[0]
    extra = request.POST.get('extra_question', '')
    comments = request.POST.get('comments', '')
    if len(extra) < 1 or len(comments) < 1:
        messages.error(request, "A field was too short!")
        return redirect('meeting')
    if not email.endswith('@buffalo.edu'):
        messages.error(request, "Must be a UB email")
        return redirect('meeting')
    if len(email) < 14:
        messages.error(request, "Email is too short")
        return redirect('meeting')

    if not User.objects.filter(email=email).first():
        ubit = str(email).split('@')[0]
        name_list = get_name(ubit)
        if None in name_list:
            messages.error(request, "That name was not found")
            return redirect('meeting')
        user = User.objects.create_user(ubit, email, random_generator(), first_name=name_list[0],
                                        last_name=name_list[1])
        user.save()
        profile = Profile.objects.create(attended=0, user=user, phone_number="00")
        profile.save()
        user.profile.save()
    else:
        user = User.objects.filter(email=email).first()

    # See if they already submitted
    if meeting.responses.filter(user=User.objects.filter(email=email).first()).first():
        messages.error(request, "That email is already used for a submission")
        return redirect('meeting')
    meeting_response = Response.objects.create(user=user, meeting=meeting, extra_question_answer=extra, comments=comments)
    meeting_response.save()
    user.profile.attended += 1
    user.save()
    user.profile.save()
    messages.success(request, 'Thank you for your submission!')
    return redirect('meeting')


def handler404(request):
    messages.error(request, "Uh oh! That page doesn't exist")
    return redirect('index')


def handler500(request):
    messages.error(request, "Uh oh! Something went wrong!")
    return redirect('index')
