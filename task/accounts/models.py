from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments")
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("confirmed", "Confirmed")], default="pending")

    def __str__(self):
        return f"Appointment between {self.patient} and {self.doctor} on {self.date}"
