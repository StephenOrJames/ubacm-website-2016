import datetime
from django.contrib.auth.models import User
from django.db.models import Model, CharField, DateField, TextField, ManyToManyField, ImageField, ForeignKey, CASCADE, BooleanField


class Event(Model):
    name = CharField(max_length=64, default="")
    location = CharField(max_length=64, default="")
    description = TextField(default="", help_text="Please include a contact email/phone", max_length=256)
    time = CharField(default="", max_length=10)
    date = DateField(default=datetime.date.today)
    link = CharField(default="", max_length=128, help_text="This can be blank. If not, needs http:// and all", blank=True)
    picture = ImageField(upload_to="events/images/", null=True, blank=True, help_text="Optional, but can be used.")

    class Meta:
        db_table = "events"
        ordering = ['-date',]


class Meeting(Model):
    # See who came
    date = DateField(default=datetime.date.today)
    overview = TextField(default="")
    extra_question = CharField(default="What is your favorite movie?", max_length=120)
    is_open = BooleanField(default=False)

    @property
    def attendance(self):
        return len(self.responses.all())

    class Meta:
        db_table = 'meetings'
        ordering = ['-date',]


class Response(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='responses')
    extra_question_answer = TextField(default="")
    meeting = ForeignKey(Meeting, related_name="responses", on_delete=CASCADE)
    comments = TextField(default="", null=True, blank=True)

    class Meta:
        db_table = 'responses'
