from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm, BlogForm
from .models import CustomUser, Appointment, Blog
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

@login_required
def create_blog_post(request):
    if request.user.user_type != 'doctor':
        return redirect('dashboard')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('doctor_blogs')
    else:
        form = BlogForm()
    return render(request, 'accounts/create_blog_post.html', {'form': form})

@login_required
def doctor_blogs(request):
    if request.user.user_type != 'doctor':
        return redirect('dashboard')
    posts = Blog.objects.filter(author=request.user)
    return render(request, 'accounts/doctor_blogs.html', {'posts': posts})

@login_required
def edit_blog_post(request, blog_id):
    blog_post = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('doctor_blogs')
    else:
        form = BlogForm(instance=blog_post)
    return render(request, 'accounts/create_blog_post.html', {'form': form, 'edit': True})

@login_required
def delete_blog_post(request, blog_id):
    blog_post = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        blog_post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('doctor_blogs')
    return render(request, 'accounts/confirm_delete_blog.html', {'blog': blog_post})

@login_required
def patient_blogs(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    posts = Blog.objects.filter(is_draft=False)
    if q:
        posts = posts.filter(title__icontains=q) | posts.filter(summary__icontains=q) | posts.filter(content__icontains=q)
    if category:
        posts = posts.filter(category=category)
    categories = Blog.CATEGORY_CHOICES
    return render(request, 'accounts/patient_blogs.html', {'posts': posts, 'categories': [dict(name=c[1], value=c[0]) for c in categories]})
