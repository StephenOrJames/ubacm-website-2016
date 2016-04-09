from django.contrib import admin
from django import forms
from pagedown.widgets import AdminPagedownWidget

from blog.models import Post


class PostModelForm(forms.ModelForm):
    markdown = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Post
        exclude = ['identity', 'html_file']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'posted_at')
    search_fields = ('title', 'posted_at')
    form = PostModelForm

admin.site.register(Post, PostAdmin)
