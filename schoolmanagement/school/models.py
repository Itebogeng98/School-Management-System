from django.db import models
from django.contrib.auth.models import User
from datetime import time


# --- CORE MODELS ---
class Attendance(models.Model):
    roll = models.CharField(max_length=10, null=True)
    date = models.DateField()
    cl = models.CharField(max_length=10)
    present_status = models.CharField(max_length=10)


class Notice(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=20, null=True, default='school')
    message = models.CharField(max_length=500)

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.name} - {self.location}"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()  # remove editable=False
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.TextField()
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.username} - {self.room.name} on {self.date}"


class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fixed', 'Fixed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Room, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_images/', null=True, blank=True)  # ✅ keep this
    is_resolved = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue in {self.room} by {self.user}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class UsageStats(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    usage_count = models.PositiveIntegerField(default=0)


class IssueStats(models.Model):
    total_issues = models.PositiveIntegerField()
    resolved_issues = models.PositiveIntegerField()
    unresolved_issues = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.subject} with {self.lecturer.username} on {self.day} from {self.start_time} to {self.end_time}"

