from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.username


User = get_user_model()
CATEGORY_CHOICES = [
    ('Mental Health', 'Mental Health'),
    ('Heart Disease', 'Heart Disease'),
    ('Covid19', 'Covid19'),
    ('Immunization', 'Immunization'),
]


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    speciality = models.CharField(max_length=100, default="General")
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically calculate end time (appointment duration = 45 mins)
        self.end_time = (datetime.combine(self.appointment_date, self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} - {self.appointment_date}"


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=100, choices=[
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    ])
    summary = models.TextField(max_length=255)
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def truncated_summary(self):
        words = self.summary.split()
        return ' '.join(words[:15]) + ('...' if len(words) > 15 else '')

    def __str__(self):
        return self.title


