from django.urls import path
from .api import (
    FeedbackApi,
    FeedbackFormApi,
    FeedbackFormElementApi,
    PlacementApi,
)

urlpatterns = [
    path('', FeedbackFormApi.as_view(), name='feedback-forms'),
    path('<uuid:form_id>/', FeedbackFormApi.as_view(), name='feedback-form'),
    path('key/<str:form_key>/', FeedbackFormApi.as_view(), name='feedback-form-by-key'),
    path('placements/', PlacementApi.as_view(), name='feedback-placements'),
    path('element/', FeedbackFormElementApi.as_view(), name='feedback-element'),
    path('submit/<uuid:form_id>/', FeedbackApi.as_view(), name='feedback-collect'),
    path('submit/<uuid:form_id>/placement/<str:placement_id>/', FeedbackApi.as_view(), name='feedback-place-collect'),
    path('submit/<str:form_id>/', FeedbackApi.as_view(), name='feedback-collect-by-key'),
    path('submit/<str:form_id>/placement/<str:placement_id>/', FeedbackApi.as_view(), name='feedback-place-collect-by-key'),

]
