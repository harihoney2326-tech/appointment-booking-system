from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available_days = models.CharField(
        max_length=100,
        help_text="e.g. Mon,Tue,Wed,Thu,Fri"
    )
    start_time = models.TimeField(help_text="Doctor available from this time")
    end_time = models.TimeField(help_text="Doctor available till this time")
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents two patients booking the SAME doctor at the SAME date+time
        unique_together = ('doctor', 'date', 'time')
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.username} -> {self.doctor.name} on {self.date} {self.time}"
