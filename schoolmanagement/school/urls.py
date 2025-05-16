from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('lecturer_login/', views.lecturer_login, name='lecturer_login'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_register/', views.student_register, name='student_register'),
    path('lecturer_register/', views.lecturer_register, name='lecture_register'),
    path('admin/register/', views.admin_register, name='admin_register'),
    path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('book-room/', views.book_room, name='book_room'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/booking/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('admin/issues/', views.admin_issues, name='admin_issues'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/user-management/', views.admin_user_management, name='admin_user_management'),
    path('admin/analytics/', views.admin_analytics, name='admin_analytics'),
    path('school/admin/notifications/', views.admin_notifications, name='admin_notifications'),
    # lecturer
    path('lecturer/timetable/', views.lecturer_timetable, name='lecturer_timetable'),
    path('lecturer/lecturer_bookings/', views.lecturer_bookings, name='lecturer_bookings'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('mark-fixed/<int:issue_id>/', views.mark_issue_fixed, name='mark_issue_fixed'),
    path('lecturer_notifications/', views.lecturer_notifications, name='lecturer_notifications'),
    path('today-schedule/', views.todays_schedule, name='todays_schedule'),
    
    # Student
    path('student_announcement/', views.student_announcement, name='student_announcement'),
    

]
