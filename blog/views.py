from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.template.response import TemplateResponse
from itertools import chain

from contacts.models import Profile
from lib import check_lengths, random_generator

from blog.models import Post, PostRequest
from lib.ubitscrap import get_name


def index(request):
    if request.method == 'POST':
        posts1 = Post.objects.filter(title__icontains=request.POST.get('search', '')).all()
        posts2 = Post.objects.filter(description__icontains=request.POST.get('search', '')).all()
        blogs = posts1 | posts2
    else:
        posts = Post.objects.all()
        paginator = Paginator(posts, 15)
        page = int(request.GET.get('page', 1))
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            blogs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            blogs = paginator.page(paginator.num_pages)
    return render(request, 'blog.html', {'posts': blogs})


def view_post(request, identity):
    if not identity or len(identity) < 15:
        messages.error(request, "The identity was either missing or not found.")
        return redirect('blog:index')
    post = Post.objects.filter(identity=identity).first()
    if post:
        intro = "{% extends 'blogpost.html' %} {% block markdown %}"
        template = Template(intro + str(post.html_file.read().decode('utf-8')) + "{% endblock %}")
        post.html_file.close()
        return TemplateResponse(request, template, {'post': post})
        # return render(request, 'blogpost.html', {'post': post})
    messages.error(request, "The identity was either missing or not found.")
    return redirect('blog:index')


def request_post(request):
    if request.method == 'POST':
        file = request.FILES['file']
        title = request.POST.get('title', "")
        description = request.POST.get('description', "")
        email = request.POST.get('email', "")
        if not file or not check_lengths(title, description, email):
            messages.error(request, "Something does not look right; either too short or empty.")
            return redirect('blog:request')
        user = User.objects.filter(email=email).first()
        if not user:
            if not email.endswith('@buffalo.edu'):
                messages.error(request, "Must be a UB email")
                return redirect('blog:request')
            if len(email) < 14:
                messages.error(request, "Email is too short")
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
        # User exists here, file and fields are good.
        fileContents = ""
        for chunk in file.chunks():
            fileContents += str(chunk.decode("utf-8"))
        prequest = PostRequest.objects.create(title=title, description=description, author=user, markdown=fileContents)
        prequest.save()
        messages.success(request, "Your request was sent!")
        return redirect('blog:index')
    elif request.method == 'GET':
        return render(request, 'request.html')
