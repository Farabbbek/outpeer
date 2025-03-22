from django.urls import path
from .views import courses_list, create_course, add_student, remove_student

urlpatterns = [
    path('', courses_list, name='courses_list'),  
    path('create/', create_course, name='create_course'),
    path('<int:course_id>/add_student/', add_student, name='add_student'), 
    path('<int:course_id>/remove_student/', remove_student, name='remove_student'),  
    ]

