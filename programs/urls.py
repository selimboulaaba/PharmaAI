from django import views
from django.urls import path
from .views import (
    PersonalRecommendationView,
    ProgramListView, 
    ProgramDetailView,
    ProgramCreateView,
    ProgramUpdateView,
    ProgramDeleteView,
    
)

urlpatterns = [
    path('', ProgramListView.as_view(), name='program_list'),
    path('program/<int:pk>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program/new/', ProgramCreateView.as_view(), name='program_create'),
    path('program/<int:pk>/edit/', ProgramUpdateView.as_view(), name='program_update'),
    path('program/<int:pk>/delete/', ProgramDeleteView.as_view(), name='program_delete'),
    path('get-recommendation/', PersonalRecommendationView.as_view(), name='get_recommendation'),


]