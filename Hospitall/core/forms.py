from django import forms
from .models import UserAbs,Patients
from django.contrib.auth.models import User

# class UserAbsForm(forms.ModelForm):
#     class Meta:
#         model=UserAbs
#         fields='__all__'
class UserForm(forms.ModelForm):
    class Meta:
        model=UserAbs
        fields=["username","mobile_number","gender", "email", "password"]


class PatientForm(forms.ModelForm):
    class Meta:
        model=Patients
        fields='__all__'

    # usernames = forms.CharField(max_length=20)
    # password=forms.CharField(max_length=20)
    # name=forms.CharField(max_length=50)
    # user_email=forms.CharField(max_length=20)
    # address=forms.CharField(max_length=100)
    # mobile_number = forms.CharField(max_length=11)


    
    


    