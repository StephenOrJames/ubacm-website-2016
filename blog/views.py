from django.contrib import messages
from django.shortcuts import render, redirect

from blog.models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog.html', {'posts': posts})


def view_post(request, identity):
    if not identity or len(identity) < 15:
        messages.error(request, "The identity was either missing or not found.")
        return redirect('blog:index')
    post = Post.objects.filter(identity=identity).first()
    if post:
        return render(request, 'blogpost.html', {'post': post})
    messages.error(request, "The identity was either missing or not found.")
    return redirect('blog:index')
