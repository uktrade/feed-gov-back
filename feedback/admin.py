from django.contrib import admin
from .models import FeedbackForm, FormElement, FeedbackData


class FeedbackFormAdmin(admin.ModelAdmin):
    pass


class FormElementAdmin(admin.ModelAdmin):
    pass


class FeedbackDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(FeedbackForm, FeedbackFormAdmin)
admin.site.register(FormElement, FormElementAdmin)
admin.site.register(FeedbackData, FeedbackFormAdmin)
