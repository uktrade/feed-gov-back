from django.urls import path
from .api import (
    FeedbackApi,
    FeedbackFormApi,
    FeedbackFormElementApi
)

urlpatterns = [
    path('', FeedbackFormApi.as_view(), name='feedback-form'),
    path('element/', FeedbackFormElementApi.as_view(), name='feedback-element'),

]
