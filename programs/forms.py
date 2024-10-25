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
        image = forms.ImageField(required=False)

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'sets', 'reps', 'order']
        widgets = {
            'order': forms.HiddenInput()  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  
            program = kwargs.get('instance', None)
            if program:
                self.initial['order'] = Exercise.objects.filter(program=program).count()
            else:
                self.initial['order'] = 0

ExerciseFormSet = inlineformset_factory(
    FitnessProgram,
    Exercise,
    form=ExerciseForm,
    fields=['name', 'description', 'sets', 'reps', 'order'],
    extra=1,
    can_delete=True
)
