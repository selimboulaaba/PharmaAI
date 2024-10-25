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
