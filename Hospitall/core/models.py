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

    def __str__(self) :
        return f"{self.user.username}"

class Doctors(UserAbs):
    address = models.TextField()
    expertise = models.CharField(max_length=50)
    work_experienc = models.IntegerField()
    visit_price = models.DecimalField(max_digits=20, decimal_places=2)
    

