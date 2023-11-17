from django.db import models
# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser,UserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password

class UserMan(UserManager):
    def create_superuser(self, username,mobile_number,gender, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username,mobile_number,gender, email, password, **extra_fields)
    
    
    def _create_user(self, username,mobile_number,gender, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username,mobile_number=mobile_number,gender=gender, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

class UserAbs(AbstractUser):
    objects = UserMan
    REQUIRED_FIELDS = ["email","mobile_number","gender"]
    mobile_number = models.CharField(max_length=11)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


class Patients(models.Model):
    user_id=models.OneToOneField("UserAbs",on_delete=models.CASCADE,related_name='Patients')
    address = models.TextField()

    def __str__(self) :
        return f"{self.user.username}"

class Doctors(models.Model):
    user_id=models.OneToOneField("UserAbs",on_delete=models.CASCADE,related_name='Doctors')
    address = models.TextField()
    expertise = models.CharField(max_length=50)
    work_experienc = models.IntegerField()
    visit_price = models.DecimalField(max_digits=20, decimal_places=2)
    

