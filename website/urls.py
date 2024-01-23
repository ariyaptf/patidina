from django.urls import path
from . import views

urlpatterns = [
    path(
        'ajax/cal/events/',
        views.today_message_get_calendar_events,
        name='today_message_get_calendar_events',
    ),
    path('api/events/', views.events_api, name='events_api'),
    path('test-sms/', views.TestSms.as_view(), name='test_sms'),
    path('otp-form/', views.show_otp_form, name='show_otp_form'),
    path('send-otp/', views.send_otp, name='send_otp'),
]
