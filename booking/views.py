from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
import datetime

from .models import Doctor, Appointment
from .forms import PatientRegisterForm, AppointmentForm


def home(request):
    doctor_count = Doctor.objects.count()
    return render(request, 'booking/home.html', {'doctor_count': doctor_count})


def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome.")
            return redirect('doctor_list')
    else:
        form = PatientRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'booking/doctor_list.html', {'doctors': doctors})


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user

            # Block booking in the past
            if appointment.date < datetime.date.today():
                messages.error(request, "You cannot book an appointment in the past.")
                return render(request, 'booking/book_appointment.html', {'doctor': doctor, 'form': form})

            try:
                appointment.save()
                messages.success(request, f"Appointment requested with Dr. {doctor.name} on {appointment.date} at {appointment.time}.")
                return redirect('my_appointments')
            except IntegrityError:
                messages.error(request, "That slot is already booked. Please choose a different time.")
    else:
        form = AppointmentForm()

    return render(request, 'booking/book_appointment.html', {'doctor': doctor, 'form': form})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'booking/my_appointments.html', {'appointments': appointments})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    appointment.status = 'CANCELLED'
    appointment.save()
    messages.info(request, "Appointment cancelled.")
    return redirect('my_appointments')
