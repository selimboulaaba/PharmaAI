
from django import views
from django.urls import path

from schedule.views import ScheduleCalendarView, ScheduleCreateView, ScheduleDeleteView, ScheduleUpdateView



urlpatterns = [
 
path('schedule/', ScheduleCalendarView.as_view(), name='schedule_calendar'),
path('schedule/add/', ScheduleCreateView.as_view(), name='schedule_create'),
path('schedule/<int:pk>/update/', ScheduleUpdateView.as_view(), name='schedule_update'),
path('schedule/<int:pk>/delete/', ScheduleDeleteView.as_view(), name='schedule_delete'),


]
