from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from contacts.models import Profile
from events.models import Event


class ContactInline(admin.StackedInline):
    model = Profile


class UserDisplay(UserAdmin):
    inlines = (ContactInline,)

admin.site.unregister(User),
admin.site.register(User, UserDisplay)


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", 'location', 'date', 'time')
    search_fields = ("name", "location", "time")

admin.site.register(Event, EventAdmin)
