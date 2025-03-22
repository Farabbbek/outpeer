from django.urls import path
from .views import register, confirm, user_list, course_list

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm/', confirm, name='confirm'),
    path('list/', user_list, name='user_list'),
    path('courses/', course_list, name='course_list'),
]