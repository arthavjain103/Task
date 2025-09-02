from django.urls import path
from .views import signup_view, login_view, dashboard_view, logout_view, patient_dashboard_view, doctor_dashboard_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
   
    path("patient_dashboard/", patient_dashboard_view, name="patient_dashboard"),
    path("doctor_dashboard/", doctor_dashboard_view, name="doctor_dashboard"),
]
