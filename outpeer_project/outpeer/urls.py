from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')), 
    path('api/', include('lessons.urls')),
    path('', lambda request: redirect('users/register/')), 
]
