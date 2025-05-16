from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Booking,Notification,Issue
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from . import forms
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentUserForm,AdminUserForm,LecturerUserForm,BookingForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from collections import Counter
from .models import Issue
from .forms import IssueForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification, Timetable  # Imported Timetable as you indicated
from django.utils import timezone
from django.shortcuts import render
from .models import Timetable
import datetime



# def home_view(request):
#     return render(request, 'school/landing.html')


# def home_view(request):
#     return HttpResponse("<html><body><h1>Test Page</h1></body></html>", content_type="text/html")

from django.shortcuts import render

def home_view(request):
    return render(request, 'school/landing.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None and user.is_superuser:
                login(request, user)
                return render(request, 'school/admin_dashboard.html')
            else:
                messages.error(request, 'Access denied. This login is for admins only.')
        else:
            messages.error(request, 'Error validating the form.')
    else:
        form = AuthenticationForm()
    return render(request, 'school/admin_login.html', {'form': form})



def student_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None and not user.is_staff and not user.is_superuser:
                login(request, user)
                return render(request, 'school/student_dashboard.html')
            else:
                messages.error(request, 'Access denied. This login is for students only.')
        else:
            messages.error(request, 'Error validating the form.')
    else:
        form = AuthenticationForm()
    return render(request, 'school/student_login.html', {'form': form})

def lecturer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None and user.is_staff and not user.is_superuser:
                login(request, user)
                return render(request, 'school/lecturer_dashboard.html')
            else:
                messages.error(request, 'Access denied. This login is for lecturers only.')
        else:
            messages.error(request, 'Error validating the form.')
    else:
        form = AuthenticationForm()
    return render(request, 'school/lecturer_login.html', {'form': form})





def student_register(request):
    if request.method == 'POST':
        form = StudentUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.is_staff = False  # Students don't have admin privileges
            user.is_superuser = False
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('student_login')
    else:
        form = StudentUserForm()
    return render(request, 'school/student_register.html', {'form': form})

def lecturer_register(request):
    if request.method == 'POST':
        form = LecturerUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_staff = True  # Optional: Allow admin panel access
            user.is_superuser = False  # Make sure they're not a superuser
            user.save()
            messages.success(request, "Lecturer registration successful. Please log in.")
            return redirect('lecturer_register')
    else:
        form = LecturerUserForm()
    return render(request, 'school/lecturer_register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.is_staff = True  # Makes the user an admin
            user.is_superuser = True  # Grants full admin privileges
            user.save()
            messages.success(request, "Admin registration successful. Please log in.")
            return redirect('admin_login')
    else:
        form = AdminUserForm()
    return render(request, 'school/admin_register.html', {'form': form})


def user_logout(request):
    logout(request)  # Log out the user
    request.session.flush()  # Completely clears the session data
    return redirect('home_view')  # Redirect to dashboard


# @login_required

def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Room booked successfully!")
            return render(request, 'school/book_room.html')  # Or any relevant URL name
    else:
        form = BookingForm()
    
    return render(request, 'school/book_room.html', {'form': form})


# @login_required
def admin_bookings(request):
    if not request.user.is_superuser:
        return redirect('admin_dashboard')  # use redirect, not render, for nav flow

    bookings = Booking.objects.all()
    issues = Issue.objects.all()

    return render(request, 'school/admin_bookings.html', {
        'bookings': bookings,
        'issues': issues
    })


def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_approved = True
    booking.save()
    return redirect('admin_bookings')

# @login_required
def admin_issues(request):
    issues = Issue.objects.all().order_by('-created_at')
    return render(request, 'school/admin_issues.html', {'issues': issues})

def admin_dashboard(request):
    return render(request, 'school/admin_dashboard.html')


# @login_required
def admin_user_management(request):
    users = User.objects.all()
    return render(request, 'school/admin_user_management.html', {'users': users})



from django.shortcuts import render
from django.contrib.auth.models import User, Group
from collections import Counter
from .models import Booking, Issue

from datetime import datetime

def admin_analytics(request):
    total_users = User.objects.count()
    students = Group.objects.get(name="Student").user_set.count() if Group.objects.filter(name="Student").exists() else 0
    lecturers = Group.objects.get(name="Lecturer").user_set.count() if Group.objects.filter(name="Lecturer").exists() else 0
    admins = User.objects.filter(is_superuser=True).count()

    # Room booking stats (weekly)
    room_booking_counts = [0] * 7  # Monday = 0, Sunday = 6
    bookings = Booking.objects.all()
    for booking in bookings:
        if hasattr(booking, 'date') and booking.date:
            weekday = booking.date.weekday()
            room_booking_counts[weekday] += 1

    # Issue status stats (based on 'is_resolved')
    issues = Issue.objects.all()
    issue_status_counts = {
        "Resolved": issues.filter(is_resolved=True).count(),
        "Pending": issues.filter(is_resolved=False).count(),
    }

    context = {
        'total_users': total_users,
        'students': students,
        'lecturers': lecturers,
        'admins': admins,
        'room_booking_counts': room_booking_counts,
        'issue_status_counts': issue_status_counts,
    }
    return render(request, 'school/admin_analytics.html', context)




@login_required
def admin_notifications(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Notification.objects.create(
                user=request.user,  # assumes the admin is logged in
                message=message,
                timestamp=timezone.now()
            )
            return redirect('admin_notifications')  # adjust to match your URL name

    notifications = Notification.objects.all().order_by('-timestamp')
    return render(request, 'school/admin_notifications.html', {'notifications': notifications})

# ===================================lecturer views(functions)====================================================================

def lecturer_timetable(request):
    timetable = Timetable.objects.filter(lecturer=request.user)
    return render(request, 'school/lecturer_timetable.html', {'timetable': timetable})

# def lecturer_bookings(request):
#     if not request.user.is_superuser:
#         return render('school/admin_bookings.html')
#     bookings = Booking.objects.all()
#     return render(request, 'school/admin_bookings.html', {'bookings': bookings})

def lecturer_bookings(request):
    # Only show bookings for this lecturer
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'school/lecturer_bookings.html', {'bookings': bookings})

def report_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('report_issue')  # Redirect after submission
    else:
        form = IssueForm()
    return render(request, 'school/report_issue.html', {'form': form})

# @login_required
def mark_issue_fixed(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    issue.is_resolved = 'fixed'
    issue.save()
    return redirect('admin_issues')

@login_required
def lecturer_notifications(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Notification.objects.create(
                user=request.user,  # assumes the user is logged in
                message=message,
                timestamp=timezone.now()
            )
            return redirect('lecturer_notifications')  # adjust to match your URL name

    notifications = Notification.objects.all().order_by('-timestamp')
    return render(request, 'school/lecturer_notifications.html', {'notifications': notifications})

@login_required
def todays_schedule(request):
    today = timezone.now().strftime('%A')  # e.g., "Monday"

    # Optionally filter by logged-in user if they are a lecturer
    if request.user.is_authenticated:
        schedule = Timetable.objects.filter(day=today, lecturer=request.user)
    else:
        schedule = Timetable.objects.filter(day=today)

    context = {
        'schedule': schedule,
    }
    return render(request, 'schedule/todays_schedule.html', context)

# ===================================Student views(functions)====================================================================
@login_required
def student_announcement(request):
    notifications = Notification.objects.all().order_by('-timestamp')
    return render(request, 'school/student_announcement.html', {'notifications': notifications})

@login_required
def dashboard_view(request):
    student = request.user
    today = timezone.now().date()

    classes_today = Booking.objects.filter(
        student=student,
        start_time__date=today
    ).count()
    print("==============context=========================")

    upcoming_bookings = Booking.objects.filter(
        student=student,
        start_time__date__gt=today
    ).count()

    context = {
        'classes_today': classes_today,
        'upcoming_bookings': upcoming_bookings,
    }

    return render(request, 'dashboard.html', context)

