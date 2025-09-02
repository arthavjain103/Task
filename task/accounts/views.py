from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import CustomUser, Appointment
from django.utils.timezone import now

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard_view(request):
    """Redirect user to the correct dashboard"""
    user = request.user
    if user.user_type == "patient":
        return redirect("patient_dashboard")
    elif user.user_type == "doctor":
        return redirect("doctor_dashboard")
    return redirect("login")

@login_required
def patient_dashboard_view(request):
    """Patient dashboard with doctor list + booking appointments"""
    user = request.user
    if user.user_type != "patient":
        return redirect("dashboard")

    doctors = CustomUser.objects.filter(user_type="doctor")
    appointments = Appointment.objects.filter(patient=user).select_related("doctor")

    if request.method == "POST":
        doctor_id = request.POST.get("doctor_id")
        appointment_date = request.POST.get("appointment_date")
        if doctor_id and appointment_date:
            try:
                doctor = CustomUser.objects.get(id=doctor_id, user_type="doctor")
                Appointment.objects.create(
                    patient=user,
                    doctor=doctor,
                    date=appointment_date
                )
                messages.success(request, "Appointment booked successfully!")
            except CustomUser.DoesNotExist:
                messages.error(request, "Selected doctor does not exist.")
        return redirect("patient_dashboard")

    return render(
        request,
        "accounts/patient_dashboard.html",
        {
            "user": user,
            "doctors": doctors,
            "appointments": appointments,
            "upcoming_count": appointments.filter(date__gte=now()).count(),
        }
    )

@login_required
def doctor_dashboard_view(request):
    """Doctor dashboard showing appointments with patients"""
    user = request.user
    if user.user_type != "doctor":
        return redirect("dashboard")

    appointments = Appointment.objects.filter(doctor=user).select_related("patient")

    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id")
        if appointment_id:
            try:
                appointment = Appointment.objects.get(id=appointment_id, doctor=user, status="pending")
                appointment.status = "confirmed"
                appointment.save()
                messages.success(request, "Appointment confirmed successfully!")
            except Appointment.DoesNotExist:
                messages.error(request, "Appointment not found or already confirmed.")
        return redirect("doctor_dashboard")

    return render(
        request,
        "accounts/doctor_dashboard.html",
        {
            "user": user,
            "appointments": appointments,
            "upcoming_count": appointments.filter(date__gte=now()).count(),
        }
    )
