from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from contacts.models import IdeaMachine
from lib import random_generator


def easy_signup(request):
    """
    This is accessible only by Admins
    :param request:
    :return:
    """
    return render(request, 'easy_signup.html')


def easy_signup_post(request):
    if request.method != 'POST':
        return redirect('index')
    data = {
        'email': request.POST.get('email', ''),
        'first': str(request.POST.get('first', '')),
        'last': str(request.POST.get('last')),
        'idea': str(request.POST.get('description', ''))
    }
    if User.objects.filter(email=data['email']).first() is not None:
        messages.error(request, "User already exists!")
        return redirect('easy_signup')
    if len(data['email']) < 3 or len(data['first']) < 3 or len(data['last']) < 3:
        messages.error(request, "Something was too short!")
        return redirect('easy_signup')
    user = User.objects.create_user(data['email'].split('@')[0], data['email'], random_generator(),
                                    first_name=data['first'], last_name=data['last'])
    user.save()
    if len(data['idea']) > 3:
        idea = IdeaMachine.objects.create(text=data['idea'])
        idea.save()
    messages.success(request, "Thanks for signing up!")
    return redirect('easy_signup')
