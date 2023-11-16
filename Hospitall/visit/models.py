from django.db import models
from core.models import Patients,Doctors

# Create your models here.
class Visit_date(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='visit_date')
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='visit_date')
    visit_time=models.DateTimeField()
    def __str__(self):
        return f"{self.visit_time}"

class Medical_record(models.Model): 
    record_time=models.DateTimeField(auto_now_add=True)
    record_time_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.record_time}"

class Visit_forms(models.Model):
    name=models.CharField(max_length=100)
    visit_desc=models.TextField()
    hospitalization=models.BooleanField()
    duration_of_hospitalization=models.IntegerField
    medical_records = models.ForeignKey(Medical_record, on_delete=models.CASCADE, related_name='Visit_forms')
    visit_dates_id = models.ForeignKey(Visit_date, on_delete=models.CASCADE, related_name='Visit_forms')

    def __str__(self):
        return f"{self.name}_{self.pk}"







    
    



