from django.contrib import admin
from .models import Patients,Doctors,UserAbs

# Register your models here.
admin.site.register(Patients)
admin.site.register(Doctors)
admin.site.register(UserAbs)



