from django.urls import path
from . import views

urlpatterns = [
    # API views
    path('api/courses/', views.course_list, name='course_list'),
    path('api/courses/<int:course_id>/lessons/', views.lessons_by_course, name='lessons_by_course'),
    path('api/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('api/lessons/create/', views.create_lesson, name='create_lesson'),
    path('api/lessons/<int:lesson_id>/update/', views.update_lesson, name='update_lesson'),
    path('api/lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson_api'),

    # HTML views
    path('api/lessons/', views.all_lessons_view, name='lessons_list'),  # Для /api/lessons/
    path('courses/<int:course_id>/lessons/', views.lessons_html_view, name='lessons-by-course'),
    path('courses/<int:course_id>/lessons/create/', views.create_lesson_html, name='create_lesson_html'),
    path('course/<int:course_id>/add/', views.add_lesson, name='add_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
]