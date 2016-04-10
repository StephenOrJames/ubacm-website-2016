from django.contrib.auth.models import User
from django.db.models import Model, CharField, IntegerField, ForeignKey, CASCADE, TextField, OneToOneField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name="profile", null=True)
    phone_number = CharField(max_length=12, default="", help_text="")
    attended = IntegerField(default=0)

    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = "contacts"
