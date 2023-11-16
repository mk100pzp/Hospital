from django.db import models
from core.models import Patients

# Create your models here.
class Bill(models.Model):
   patients=models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='bill')  
   date=models.DateTimeField(auto_now_add=True)
   patient_share=models.DecimalField(max_digits=20, decimal_places=2)
   amount_paid=models.DecimalField(max_digits=20, decimal_places=2)
   the_remaining_amount=models.DecimalField(max_digits=20, decimal_places=2)
   insurance_contribution=models.DecimalField(max_digits=20, decimal_places=2)
   def __str__(self):
        return f"{self.patients}"

