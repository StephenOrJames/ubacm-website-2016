import datetime
import os

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from lib import random_generator
from django.contrib.auth.models import User
from django.db.models import Model, CharField, ForeignKey, TextField, CASCADE, DateField, FileField


class Post(Model):
    title = CharField(max_length=70, default="")
    description = TextField(max_length=128, default="", blank=True, help_text="Not needed, but give brief overview")
    author = ForeignKey(User, on_delete=CASCADE, related_name="posts")
    markdown = TextField(default="")
    posted_at = DateField(default=datetime.date.today)
    html = TextField(default="")
    html_file = FileField(upload_to="blog/html/", null=True)
    identity = CharField(max_length=16, default=random_generator)

    def display_html(self):
        with open(self.html_file.path, encoding='utf-8') as f:
            return f.read()

    def save(self, *args, **kwargs):
        if self.html_file:
            self.html_file.delete(False)
        filename = self.title.replace(' ', '-') + ".html"
        headers = {'Content-Type': 'text/plain'}
        if type(self.markdown) == bytes:  # sometimes body is str sometimes bytes...
            data = self.markdown
        elif type(self.markdown) == str:
            data = self.markdown.encode('utf-8')
        else:
            print("something is wrong")
            data = ""
        r = requests.post('https://api.github.com/markdown/raw', headers=headers, data=data)
        # avoid recursive invoke
        self.html = r.text.encode('utf-8')
        self.html_file.save(filename, ContentFile(r.text.encode('utf-8')), save=False)
        self.html_file.close()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        ordering = ['-posted_at']
