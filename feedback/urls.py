from django.urls import path
from . import views

urlpatterns = [
    path('submit/<uuid:form_id>/', views.submit_feedback),
    path('submit/<str:form_id>/', views.submit_feedback),
    path('submit/<uuid:form_id>/collection/<uuid:collection_id>/', views.submit_feedback),
    path('submit/<str:form_id>/collection/<uuid:collection_id>/', views.submit_feedback),
    path('submit/<uuid:form_id>/placement/<str:placement_id>/', views.submit_feedback),
    path('submit/<str:form_id>/placement/<str:placement_id>/', views.submit_feedback),

]
