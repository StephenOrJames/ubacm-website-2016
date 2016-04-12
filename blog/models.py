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
    markdown_file = FileField(upload_to="blog/markdown/", null=True, blank=True)
    identity = CharField(max_length=16, default=random_generator)

    def display_html(self):
        with open(self.html_file.path, encoding='utf-8') as f:
            return f.read()

    def save(self, *args, **kwargs):
        filename = self.title.replace(" ", "-") + "*.md"
        if self.markdown_file:
            self.markdown_file.delete(False)
        self.markdown_file.save(filename, ContentFile(self.markdown), save=False)
        # TODO: Call metalsmith instead of echo
        os.system("echo " + os.path.join(settings.BASE_DIR, 'media/blog/markdown/' + filename))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
