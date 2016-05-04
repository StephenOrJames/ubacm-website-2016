import datetime

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE, TextField, OneToOneField,\
    DateField, ImageField, BooleanField
from django.template import Context
from django.template.loader import get_template


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="profile", null=True)
    phone_number = CharField(max_length=12, default="", help_text="")
    attended = IntegerField(default=0)
    send_email = BooleanField(default=True)

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = "contacts"


class Newsletter(Model):
    subject = CharField(max_length=40, default="UB ACM Newsletter")

    intro = TextField(default="", help_text="If you want, a little paragraph about how things are going.", blank=True)

    sent_on = DateField(default=datetime.date.today)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'newsletters'
        ordering = ['-sent_on']

    def save(self, *args, **kwargs):
        plaintext = get_template('newsletter.txt')  # Text form
        htmly     = get_template('newsletter.html')  # HTML form
        for contact in User.objects.all():  # Send it to everyone
            if contact.profile.send_email:
                d = Context({'widgets': self.widgets.all(), 'newsletter': self, 'contact': contact})
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                subject, from_email, to = self.subject, 'ubsa-acm@buffalo.edu', contact.email
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        super(Newsletter, self).save(*args, **kwargs)


class InfoWidget(Model):
    title = CharField(max_length=32, default="")
    text = TextField(max_length=256, default="")
    newsletter = ForeignKey(Newsletter, related_name='widgets')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "infowidgets"
        verbose_name = "Newsletter Section"
        verbose_name_plural = "Text Widgets"

