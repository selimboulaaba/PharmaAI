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
    form=ExerciseForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=10,
    validate_max=True,
    absolute_max=15
)

class PersonalInfoForm(forms.Form):
    height = forms.IntegerField(  
        label='Height (cm)',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your height in cm'})
    )
    weight = forms.IntegerField(  
        label='Weight (kg)',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your weight in kg'})
    )
    age = forms.IntegerField(
        label='Age',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your age'})
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=[('Male', 'Male'), ('Female', 'Female')],  
        initial='Male'
    )
    blood_test = forms.FileField(
        label='Blood Test Results',
        required=True,
        widget=forms.FileInput(attrs={
            'accept': 'image/jpeg',  
            'class': 'form-control'
        }),
        help_text='Please upload a JPEG image of your blood test results'
    )
        