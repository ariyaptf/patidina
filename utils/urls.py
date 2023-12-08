from django.urls import path
from . import views

urlpatterns = [
    path('form-successfully-submitted/', views.FormSuccessfullySubmitted.as_view(), name='form_successfully_submitted'),
]