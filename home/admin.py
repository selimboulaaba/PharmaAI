from django.contrib import admin
from .models import (Appointment, AppointmentData, DepressionAnxiety, DoctorUser, mentalDisorder,
    ObesityData, obesityDisorder, pcosDisorder, Receipt, userHistory, UserProfile)

# Register your models here.
admin.site.register(DoctorUser)
admin.site.register(UserProfile)

admin.site.register(Appointment)
admin.site.register(AppointmentData)

admin.site.register(ObesityData)
admin.site.register(DepressionAnxiety)
admin.site.register(obesityDisorder)
admin.site.register(pcosDisorder)
admin.site.register(mentalDisorder)
admin.site.register(Receipt)

admin.site.register(userHistory)
