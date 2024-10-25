from django import forms
from django.forms import inlineformset_factory
from .models import FitnessProgram, Exercise

class FitnessProgramForm(forms.ModelForm):
    class Meta:
        model = FitnessProgram
        fields = ['title', 'description', 'difficulty', 'duration', 
                 'image', 'estimated_calories', 'equipment_needed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rounded-lg border-gray-300 w-full', 'rows': 4}),
            'difficulty': forms.Select(attrs={'class': 'form-select rounded-lg border-gray-300 w-full'}),
            'duration': forms.NumberInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'estimated_calories': forms.NumberInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'equipment_needed': forms.CheckboxInput(attrs={'class': 'form-checkbox rounded border-gray-300'}),
        }

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'sets', 'reps', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea rounded-lg border-gray-300 w-full', 'rows': 3}),
            'sets': forms.NumberInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'reps': forms.NumberInput(attrs={'class': 'form-input rounded-lg border-gray-300 w-full'}),
            'order': forms.HiddenInput(),
        }

ExerciseFormSet = inlineformset_factory(
    FitnessProgram,
    Exercise,
    fields=['name', 'sets', 'reps'],  
    extra=3,
    can_delete=True,
    min_num=1,  
    validate_min=True  
)


class PersonalInfoForm(forms.Form):
    height = forms.IntegerField(
        label='Height (cm)',
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    weight = forms.IntegerField(
        label='Weight (kg)',
        min_value=30,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label='Age',
        min_value=16,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    blood_test = forms.ImageField(
        label='Blood Test Result',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )