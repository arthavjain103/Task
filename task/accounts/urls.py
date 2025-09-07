from django.urls import path
from .views import signup_view, login_view, dashboard_view, logout_view, patient_dashboard_view, doctor_dashboard_view, create_blog_post, doctor_blogs, patient_blogs, edit_blog_post, delete_blog_post

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
   
    path("patient_dashboard/", patient_dashboard_view, name="patient_dashboard"),
    path("doctor_dashboard/", doctor_dashboard_view, name="doctor_dashboard"),
    path('create_blog_post/', create_blog_post, name='create_blog_post'),
    path('doctor_blogs/', doctor_blogs, name='doctor_blogs'),
    path('patient_blogs/', patient_blogs, name='patient_blogs'),
    path('edit_blog_post/<int:blog_id>/', edit_blog_post, name='edit_blog_post'),
    path('delete_blog_post/<int:blog_id>/', delete_blog_post, name='delete_blog_post'),
]
