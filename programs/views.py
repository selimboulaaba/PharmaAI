from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import FitnessProgram, Exercise
from .forms import FitnessProgramForm, ExerciseFormSet

class ProgramListView(ListView):
    model = FitnessProgram
    template_name = 'fitness/program_list.html'
    context_object_name = 'programs'
    paginate_by = 9

    def get_queryset(self):
        queryset = FitnessProgram.objects.all().order_by('-created_at')
        
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        duration = self.request.GET.get('duration')
        if duration:
            if duration == 'short':
                queryset = queryset.filter(duration__lt=30)
            elif duration == 'medium':
                queryset = queryset.filter(duration__range=(30, 60))
            elif duration == 'long':
                queryset = queryset.filter(duration__gt=60)
                
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        return queryset

class ProgramDetailView(DetailView):
    model = FitnessProgram
    template_name = 'fitness/program_detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['similar_programs'] = FitnessProgram.objects.filter(
            difficulty=self.object.difficulty
        ).exclude(id=self.object.id)[:3]
        return context

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = FitnessProgram
    form_class = FitnessProgramForm
    template_name = 'fitness/program_form.html'
    success_url = reverse_lazy('program_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['exercise_formset'] = ExerciseFormSet(self.request.POST)
        else:
            context['exercise_formset'] = ExerciseFormSet()
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        context = self.get_context_data()
        exercise_formset = context['exercise_formset']
        
        if exercise_formset.is_valid():
            response = super().form_valid(form)
            exercise_formset.instance = self.object
            exercise_formset.save()
            messages.success(self.request, 'Program created successfully!')
            return response
        else:
            return super().form_invalid(form)

class ProgramUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FitnessProgram
    form_class = FitnessProgramForm
    template_name = 'fitness/program_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['exercise_formset'] = ExerciseFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context['exercise_formset'] = ExerciseFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        exercise_formset = context['exercise_formset']
        
        if exercise_formset.is_valid():
            response = super().form_valid(form)
            exercise_formset.save()
            messages.success(self.request, 'Program updated successfully!')
            return response
        else:
            return super().form_invalid(form)

    def test_func(self):
        program = self.get_object()
        return self.request.user == program.creator

class ProgramDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FitnessProgram
    success_url = reverse_lazy('program_list')
    template_name = 'fitness/program_confirm_delete.html'

    def test_func(self):
        program = self.get_object()
        return self.request.user == program.creator

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Program deleted successfully!')
        return super().delete(request, *args, **kwargs)

# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import FitnessProgram, Exercise

class FitnessProgramForm(forms.ModelForm):
    class Meta:
        model = FitnessProgram
        fields = ['title', 'description', 'difficulty', 'duration', 
                 'image', 'estimated_calories', 'equipment_needed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'duration': forms.NumberInput(attrs={'min': 1}),
        }

# Create inline formset for exercises
ExerciseFormSet = inlineformset_factory(
    FitnessProgram,
    Exercise,
    fields=['name', 'description', 'sets', 'reps', 'order'],
    extra=1,
    can_delete=True
)