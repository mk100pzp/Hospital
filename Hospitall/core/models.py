from django.db import models
from django.contrib.auth.models import User

class UserAbs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=11)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        abstract = True
        

class Patients(UserAbs):
    address = models.TextField()

class Doctors(UserAbs):
    address = models.TextField()
    expertise = models.CharField(max_length=50)
    work_experienc = models.IntegerField()
    visit_price = models.DecimalField()
    

