from django.shortcuts import render
from .models import Patients,Doctors

# Create your views here.
def show_patients(request):
    all=Patients.objects.all()
    return (request,'show.html',{'all':all})

