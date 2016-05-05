from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from contacts.models import Profile
from events.models import Event, Meeting, Response


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


class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ('user', 'extra_question_answer', 'comments')


class MeetingAdmin(admin.ModelAdmin):
    list_display = ("date", "extra_question", "attendance", 'is_open')
    search_fields = ("date", "extra_question")
    inlines = [ResponseInline]

admin.site.register(Meeting, MeetingAdmin)
