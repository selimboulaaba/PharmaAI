from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class FitnessProgram(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.IntegerField(help_text="Duration in minutes")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)
    estimated_calories = models.IntegerField()
    equipment_needed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    program = models.ForeignKey(FitnessProgram, related_name='exercises', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name