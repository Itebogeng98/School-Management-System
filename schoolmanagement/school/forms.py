# forms.py in school app

from django import forms
from django.contrib.auth.models import User
from .models import Attendance, Notice, Room, Booking, Issue, Notification, UsageStats, IssueStats

# --- USER FORMS ---
class TeacherUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

from django import forms
from django.contrib.auth.models import User

class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Adjust fields as needed

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
    
class LecturerUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


# booking form 

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

# forms.py in school app

# class TeacherExtraForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = ['mobile', 'status']  # Updated fields for Teacher model

# class StudentExtraForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['roll', 'student_class', 'mobile', 'fee', 'status']  # Updated fields for Student model


# # --- CORE FORMS ---
# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['roll', 'date', 'cl', 'present_status']


# class NoticeForm(forms.ModelForm):
#     class Meta:
#         model = Notice
#         fields = ['by', 'message']





class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['location', 'description', 'image']


# class NotificationForm(forms.ModelForm):
#     class Meta:
#         model = Notification
#         fields = ['user', 'message', 'is_read']


# class UsageStatsForm(forms.ModelForm):
#     class Meta:
#         model = UsageStats
#         fields = ['room', 'usage_count']


# class IssueStatsForm(forms.ModelForm):
#     class Meta:
#         model = IssueStats
#         fields = ['total_issues', 'resolved_issues', 'unresolved_issues']
