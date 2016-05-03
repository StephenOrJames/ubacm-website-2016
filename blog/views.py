from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template, Context
from django.template.response import TemplateResponse

from blog.models import Post


def index(request):
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
