from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Blog, CustomUser, Appointment
from .forms import BlogForm, SignupForm
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .utils import create_google_calendar_event
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import os
import datetime
import pickle
from google.auth.transport.requests import Request

User = get_user_model()

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]



SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate_google_calendar():
    creds = None
    token_path = "token.pickle"  # Store the authenticated token here

    # Load saved credentials if available
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    # If there are no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES  # Provide the path to client_secret.json
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return creds


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, user_type="doctor")

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()

            
            creds = authenticate_google_calendar()
            service = build("calendar", "v3", credentials=creds)

            start_datetime = datetime.datetime.combine(appointment.appointment_date, appointment.start_time)
            end_datetime = start_datetime + datetime.timedelta(minutes=45)

            event = {
                "summary": f"Appointment with Dr. {doctor.first_name} {doctor.last_name}",
                "description": f"Patient: {request.user.first_name} {request.user.last_name}",
                "start": {"dateTime": start_datetime.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end_datetime.isoformat(), "timeZone": "UTC"},
                "attendees": [{"email": doctor.email}, {"email": request.user.email}],
            }

            event = service.events().insert(calendarId="primary", body=event).execute()

            appointment.google_event_id = event.get("id")
            appointment.save()

            return redirect('appointment_success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form, 'doctor': doctor})


@login_required
def appointment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, "appointment_success.html", {"appointment": appointment})


@login_required
def list_doctors(request):

    doctors = User.objects.filter(user_type="doctor")  # Adjust field name if different
    return render(request, 'list_doctors.html', {'doctors': doctors})


@login_required
def create_blog(request):
    if request.user.user_type != 'doctor':
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set current user as author
            blog.save()
            return redirect('my_blogs')
    else:
        form = BlogForm()

    return render(request, 'create_blog.html', {'form': form})


@login_required
def my_blogs(request):
    if request.user.user_type != 'doctor':
        return redirect('home')
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'my_blogs.html', {'blogs': blogs})



def blog_list(request):
    categorized_blogs = {}
    categories = ['Mental Health', 'Heart Disease', 'Covid19', 'Immunization']

    for category in categories:
        categorized_blogs[category] = Blog.objects.filter(category=category, is_draft=False)

    return render(request, 'patientblog.html', {'categorized_blogs': categorized_blogs})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)


    if request.user == blog.author:
        blog.delete()
        return redirect('my_blogs')

    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, f"{request.user.user_type}_dashboard.html", {'user': request.user})
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')



