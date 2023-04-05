from django.contrib import admin
from .models import Patient, PatientGroup

admin.site.register(Patient)
admin.site.register(PatientGroup)
