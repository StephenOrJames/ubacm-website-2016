import datetime
from django.contrib.auth.models import User
from django.db.models import Model, CharField, DateField, TextField, ManyToManyField, ImageField


class Event(Model):
    name = CharField(max_length=64, default="")
    location = CharField(max_length=64, default="")
    description = TextField(default="", help_text="Please include a contact email/phone", max_length=256)
    time = CharField(default="", max_length=10)
    date = DateField(default=datetime.date.today)
    link = CharField(default="", max_length=128, help_text="This can be blank. If not, needs http:// and all", blank=True)
    picture = ImageField(upload_to="events/images/", null=True, blank=True, help_text="Optional, but can be used.")

    # See who came
    attendees = ManyToManyField(User, related_name="events", blank=True)

    class Meta:
        db_table = "events"
        ordering = ['-date',]
