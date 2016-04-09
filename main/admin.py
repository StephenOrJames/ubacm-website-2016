from django.contrib import admin

from main.models import EBoard, ContactForm


class EboardAdmin(admin.ModelAdmin):
    list_display = ('year', 'president_name', 'vp_name', 'treasurer_name', 'secretary_name')

admin.site.register(EBoard, EboardAdmin)


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'sent_at')
    search_fields = ('name', 'email')

admin.site.register(ContactForm, ContactFormAdmin)
