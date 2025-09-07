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


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ("mental_health", "Mental Health"),
        ("heart_disease", "Heart Disease"),
        ("covid19", "Covid-19"),
        ("immunization", "Immunization"),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'doctor'}
    )
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title


    def truncated_summary(self):
        words = self.summary.split()
        if len(words) > 15:
            return ' '.join(words[:15]) + '...'
        return self.summary
