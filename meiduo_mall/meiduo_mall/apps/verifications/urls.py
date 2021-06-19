from django.urls import path, include, re_path

from . import views

urlpatterns = [
    re_path('sms_codes/(?P<mobile>1[3-9]\d{9})/', views.SMSCodeView.as_view()),
]