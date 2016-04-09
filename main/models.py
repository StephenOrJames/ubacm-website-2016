from django.db.models import Model, CharField, TextField, DateField, ImageField
import datetime


class BackgroundImage(Model):
    image = ImageField(upload_to="homepage/background/")

    class Meta:
        db_table = 'backgroundImages'

class EBoard(Model):
    year = CharField(default="2016-2017", max_length=9)

    president_name = CharField(max_length=32, default="")
    president_grade = CharField(max_length=32, default="")
    president_major = CharField(max_length=32, default="")
    president_site = CharField(max_length=64, default="", blank=True, help_text="All sites can be blank")
    president_picture = ImageField(upload_to="eboard/profiles/")

    vp_name = CharField(max_length=32, default="")
    vp_grade = CharField(max_length=32, default="")
    vp_major = CharField(max_length=32, default="")
    vp_site = CharField(max_length=64, default="", blank=True)
    vp_picture = ImageField(upload_to="eboard/profiles/")

    treasurer_name = CharField(max_length=32, default="")
    treasurer_grade = CharField(max_length=32, default="")
    treasurer_major = CharField(max_length=32, default="")
    treasurer_site = CharField(max_length=64, default="", blank=True)
    treasurer_picture = ImageField(upload_to="eboard/profiles/")

    secretary_name = CharField(max_length=32, default="")
    secretary_grade = CharField(max_length=32, default="")
    secretary_major = CharField(max_length=32, default="")
    secretary_site = CharField(max_length=64, default="", blank=True)
    secretary_picture = ImageField(upload_to="eboard/profiles/")

    def __str__(self):
        return "Eboard " + self.year

    class Meta:
        db_table = 'eboard'


class ContactForm(Model):
    name = CharField(max_length=65, default="")
    email = CharField(max_length=76, default="")
    phone = CharField(max_length=13, default="")
    message = TextField(default="")
    sent_at = DateField(default=datetime.date.today)

    def __str__(self):
        return "Message from " + self.name

    class Meta:
        db_table = "contactforms"
        verbose_name_plural = "Contact Page Form"
        ordering = ["-sent_at",]
