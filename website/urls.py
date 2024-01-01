from django.urls import path
from . import views

urlpatterns = [
    path(
        'ajax/cal/events/',
        views.today_message_get_calendar_events,
        name='today_message_get_calendar_events',
    ),
    path('api/events/', views.events_api, name='events_api')
]
