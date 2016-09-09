from django.contrib import admin
from contacts.models import Newsletter, InfoWidget, IdeaMachine


class WidgetAdmin(admin.StackedInline):
    model = InfoWidget
    extra = 0


class NewsLetterModel(admin.ModelAdmin):
    list_display = ('subject', 'sent_on')
    search_fields = ('subject', 'sent_on')
    exclude = ('sent_on',)

    inlines = [WidgetAdmin]

    def save_model(self, request, obj, form, change):
        if not obj.pk: # call super method if object has no primary key
            super(NewsLetterModel, self).save_model(request, obj, form, change)
        else:
            super(NewsLetterModel, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        formset.save() # this will save the children

admin.site.register(Newsletter, NewsLetterModel)


class IdeaMachineAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)

admin.site.register(IdeaMachine, IdeaMachineAdmin)
