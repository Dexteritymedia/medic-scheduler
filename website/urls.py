from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.AppointmentView.as_view(), name='make-appointment'),
    path("appointment/", views.AppointmentTemplateView.as_view(), name='appointment'),
    path("manage/", views.ManageAppointmentView.as_view(), name='manage'),
]
