from datetime import time
from django import forms
from .models import TrainingSchedule

from django import forms
from .models import TrainingSchedule

class TrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainingSchedule
        fields = ['program', 'weekday', 'start_time', 'notes']
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),  
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border rounded'}),
        }
    
    def clean_start_time(self):
        start_time_value = self.cleaned_data.get('start_time')

        if start_time_value is not None:
            return start_time_value
        
        raise forms.ValidationError("Select a valid time.")

