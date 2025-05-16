from django.contrib import admin
from django.urls import path, include
from school import views  # Make sure this matches your app name and views.py file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  # Match the actual function name in views.py
    path('school/', include('school.urls')),  # Only if you have this file set up
]
