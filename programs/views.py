from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from flask import logging, redirect
import requests
from .models import FitnessProgram, Exercise
from .forms import FitnessProgramForm, ExerciseFormSet, PersonalInfoForm

class ProgramListView(ListView):
    model = FitnessProgram
    template_name = 'fitness/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        queryset = super().get_queryset()
        difficulty = self.request.GET.get('difficulty')
        duration = self.request.GET.get('duration')
        
        if difficulty and difficulty != 'All Difficulties':
            queryset = queryset.filter(difficulty=difficulty)
        if duration:
            if duration == 'Short (< 30 mins)':
                queryset = queryset.filter(duration__lt=30)
            elif duration == 'Medium (30-60 mins)':
                queryset = queryset.filter(duration__gte=30, duration__lte=60)
            elif duration == 'Long (> 60 mins)':
                queryset = queryset.filter(duration__gt=60)
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_info_form'] = PersonalInfoForm()
        return context

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
            context['exercise_formset'] = ExerciseFormSet(
                self.request.POST,
                instance=self.object if self.object else None
            )
        else:
            context['exercise_formset'] = ExerciseFormSet(
                instance=self.object if self.object else None
            )
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        exercise_formset = context['exercise_formset']
        
        
        form.instance.creator = self.request.user
        self.object = form.save()
        
        if exercise_formset.is_valid():
            exercises = exercise_formset.save(commit=False)
            
            for exercise in exercises:
                exercise.program = self.object
                exercise.save()
            
            messages.success(self.request, f'Program "{self.object.title}" created successfully with {len(exercises)} exercises!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            context['form'] = form  
            context['exercise_formset'] = exercise_formset 
            return self.render_to_response(context)

# class ProgramCreateView(LoginRequiredMixin, CreateView):
#     model = FitnessProgram
#     form_class = FitnessProgramForm
#     template_name = 'fitness/program_form.html'
#     success_url = reverse_lazy('program_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['exercise_formset'] = ExerciseFormSet(
#                 self.request.POST,
#                 instance=self.object if hasattr(self, 'object') else None
#             )
#         else:
#             context['exercise_formset'] = ExerciseFormSet(
#                 instance=self.object if hasattr(self, 'object') else None
#             )
#             for i, form in enumerate(context['exercise_formset'].forms):
#                 form.initial['order'] = i
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         exercise_formset = context['exercise_formset']
        
#         form.instance.creator = self.request.user
        
#         if exercise_formset.is_valid():
#             print("Formset is valid")
#             self.object = form.save()
#             exercise_formset.instance = self.object
            
#             for i, exercise_form in enumerate(exercise_formset.forms):
#                 if exercise_form.is_valid() and not exercise_form.cleaned_data.get('DELETE', False):
#                     exercise_form.instance.order = i
#                     print(f"Setting order {i} for exercise {exercise_form.cleaned_data.get('name')}")
            
#             exercise_formset.save()
#             messages.success(self.request, 'Program created successfully!')
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             print("Formset errors:", exercise_formset.errors)
#             return self.form_invalid(form)

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

ExerciseFormSet = inlineformset_factory(
    FitnessProgram,
    Exercise,
    fields=['name', 'description', 'sets', 'reps', 'order'],
    extra=1,
    can_delete=True
)

class PersonalRecommendationView(View):
    template_name = 'programs/program_list.html'

    def get(self, request, *args, **kwargs):
        form = PersonalInfoForm()
        return render(request, self.template_name, {
            'personal_info_form': form,
            'programs': FitnessProgram.objects.all()  
        })

    def post(self, request, *args, **kwargs):
        form = PersonalInfoForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                files = {
                    'blood_test': request.FILES['blood_test']
                }
                data = {
                    'height': form.cleaned_data['height'],
                    'weight': form.cleaned_data['weight'],
                    'age': form.cleaned_data['age'],
                    'gender': form.cleaned_data['gender'],
                }

                api_url = 'http://localhost:8001/api'
                
                response = requests.post(api_url, files=files, data=data)

                if response.status_code == 200:
                    recommendation_data = response.json()
                    request.session['fitness_recommendation'] = recommendation_data
                    messages.success(request, 'Successfully generated personalized recommendations!')
                else:
                    messages.error(request, f'Error from API: {response.status_code} - {response.text}')
            except Exception as e:
                messages.error(request, f'Error generating recommendations: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
        
        return redirect('program_list')


# class PersonalRecommendationView(View):
#     def post(self, request, *args, **kwargs):
#         form = PersonalInfoForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             try:
#                 files = {
#                     'blood_test': request.FILES['blood_test']
#                 }
#                 data = {
#                     'height': form.cleaned_data['height'],
#                     'weight': form.cleaned_data['weight'],
#                     'age': form.cleaned_data['age'],
#                     'gender': form.cleaned_data['gender'],
#                 }

#                 api_url = 'http://localhost:8001/api'
                
#                 response = requests.post(api_url, files=files, data=data)

#                 if response.status_code == 200:
#                     recommendation_data = response.json()
#                     request.session['fitness_recommendation'] = recommendation_data
#                     messages.success(request, 'Successfully generated personalized recommendations!')
#                 else:
#                     messages.error(request, f'Error from API: {response.status_code} - {response.text}')

#             except Exception as e:
#                 messages.error(request, f'Error generating recommendations: {str(e)}')
#         else:
#             messages.error(request, 'Please correct the errors in the form.')
        
#         return redirect('program_list')
