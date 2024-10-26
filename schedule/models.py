from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta

from programs.models import FitnessProgram

class TrainingSchedule(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    TIME_SLOTS = [(i, f"{i:02d}:00") for i in range(6, 22)]  

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(FitnessProgram, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['weekday', 'start_time']
        unique_together = ['user', 'weekday', 'start_time']

    def clean(self):
        if self.start_time:
            start_datetime = datetime.combine(datetime.today(), self.start_time)
            
            program_duration_hours = self.program.duration  
            end_datetime = start_datetime + timedelta(hours=program_duration_hours)

            # overlapping = TrainingSchedule.objects.filter(
            #     user=self.user,
            #     weekday=self.weekday,
            #     start_time__lt=end_datetime.time(), 
            #     start_time__gte=self.start_time
            # ).exclude(id=self.id)

        # if overlapping.exists():
        #     raise ValidationError('This time slot overlaps with another scheduled training.')

    def __str__(self):
        return f"{self.get_weekday_display()} at {self.start_time.strftime('%H:%M')} - {self.program.title}"
