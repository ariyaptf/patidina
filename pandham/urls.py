from django.urls import path
from . import views

urlpatterns = [
    path('support/', views.SupportPublicationView.as_view(), name='support'),
    path('pandham-succes/<int:pk>/', views.SuccessView.as_view(), name='pandhamm_success'),
]
