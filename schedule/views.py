from django.forms import ValidationError
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from programs.models import FitnessProgram
from .models import TrainingSchedule
from .forms import TrainingScheduleForm

class ScheduleCalendarView(LoginRequiredMixin, ListView):
    model = TrainingSchedule
    template_name = 'schedule/schedule_calendar.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return TrainingSchedule.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TrainingScheduleForm()
        context['weekdays'] = dict(TrainingSchedule.WEEKDAY_CHOICES)
        context['time_slots'] = dict(TrainingSchedule.TIME_SLOTS)

        schedule_grid = {day: {} for day in range(7)}
        for schedule in context['schedules']:
            schedule_grid[schedule.weekday][schedule.start_time.hour] = schedule
        
        context['schedule_grid'] = schedule_grid
        print(schedule_grid)
        return context
    
class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = TrainingSchedule
    form_class = TrainingScheduleForm
    success_url = reverse_lazy('schedule_calendar')

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(f"User being set: {form.instance.user}")  
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Training scheduled successfully!')

            return JsonResponse({'success': True, 'message': 'Training scheduled successfully!'})

        except ValidationError as e:
            messages.error(self.request, str(e))

            return redirect('schedule_calendar')  

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400) 

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = TrainingSchedule
    form_class = TrainingScheduleForm
    success_url = reverse_lazy('schedule_calendar')

    def get_queryset(self):
        return TrainingSchedule.objects.filter(user=self.request.user)

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = TrainingSchedule
    template_name = 'schedule/schedule_delete.html' 
    success_url = reverse_lazy('schedule_calendar')

    def get_queryset(self):
        return TrainingSchedule.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Schedule deleted successfully!')
        return super().delete(request, *args, **kwargs)