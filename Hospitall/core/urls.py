from django.urls import path
from . import views

urlpatterns = [
    path('Patients/', views.show_patients),
    # path('details/', include('core.urls')),
    # path('visit/', include('visit.urls')),
    # path('peyment/', include('peyment.urls')),
    path('create/patient/', views.create_patient ,name="create_patient"),
    path('create/user/', views.create_user ,name="create_user"),
]