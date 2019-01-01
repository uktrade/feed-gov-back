from django.contrib import admin
from .models import (
    FeedbackForm,
    FormElement,
    FeedbackData,
    FeedbackCollection,
    Placement
)


class FeedbackFormAdmin(admin.ModelAdmin):
    pass


class FormElementAdmin(admin.ModelAdmin):
    pass


class PlacementAdmin(admin.ModelAdmin):
    pass


class FeedbackDataAdmin(admin.ModelAdmin):
    pass


class DataInlineAdmin(admin.StackedInline):
    model = FeedbackData


class FeedbackCollectionAdmin(admin.ModelAdmin):
    inlines = [
        DataInlineAdmin
    ]


admin.site.register(Placement, PlacementAdmin)
admin.site.register(FeedbackForm, FeedbackFormAdmin)
admin.site.register(FormElement, FormElementAdmin)
admin.site.register(FeedbackCollection, FeedbackCollectionAdmin)
admin.site.register(FeedbackData, FeedbackFormAdmin)
