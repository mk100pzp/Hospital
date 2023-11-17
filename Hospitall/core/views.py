from django.shortcuts import render
from .models import Patients,Doctors,UserAbs
from .forms import PatientForm,UserForm


# Create your views here.
def show_patients(request):
    all=Patients.objects.all()
    return render (request,'show.html',{'all':all})

def show_doctors(request):
    all=Doctors.objects.all()
    return render (request,'show.html',{'all':all})

# def create_patient(request):
#     if request.method == 'POST':
#         form = AuthorForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             bio = form.cleaned_data['bio']

#             author_obj = Author(name=name)
#     form_obj=PatientForm(
#         usernames = 
#     password=forms.CharField(max_length=20)
#     name=forms.CharField(max_length=50)
#     user_email=forms.CharField(max_length=20)
#     address=forms.CharField(max_length=100)
#     mobile_number = forms.CharField(max_length=11)
    
#     )

def create_patient(request):
    if request.method == 'POST':
        pass
    else:
        form_obj=PatientForm()
    return render(request,'creat.html',{'form':form_obj})

def create_user(request):
    if request.method == 'POST':
        data=request.POST
        obj_form=UserForm(data)
        if obj_form.is_valid():
            clean_data=form.cleaned_data
            obj_user=UserAbs()


        obj_form.save()

    else:
        form_obj=UserForm()
    return render(request,'creat.html',{'form':form_obj})


