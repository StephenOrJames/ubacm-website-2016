from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget

from blog.models import Post, PostRequest


class PostModelForm(forms.ModelForm):
    markdown = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Post
        exclude = ['identity', 'posted_at', 'html', 'html_file', 'markdown_file']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'posted_at')
    search_fields = ('title', 'posted_at')
    form = PostModelForm

admin.site.register(Post, PostAdmin)


class PostRequestModelForm(forms.ModelForm):
    markdown = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = PostRequest
        fields = ['title', 'author', 'description', 'markdown', 'is_approved']


class PostRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description')
    search_fields = ('title', 'author', 'description')
    form = PostRequestModelForm

admin.site.register(PostRequest, PostRequestAdmin)

