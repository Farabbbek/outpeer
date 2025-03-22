from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()

def courses_list(request):
    courses = Course.objects.all()
    users = User.objects.all()  
    return render(request, 'courses/courses_list.html', {'courses': courses, 'users': users})


def create_course(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")

        if title and description and price:
            Course.objects.create(title=title, description=description, price=price)
            messages.success(request, "Курс успешно создан!")
        else:
            messages.error(request, "Все поля должны быть заполнены!")

    return redirect('courses_list')


def add_student(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        student_id = request.POST.get("student_id")

        try:
            student = User.objects.get(id=student_id)
            if student not in course.students.all():
                course.students.add(student)
                messages.success(request, f"Студент {student.email} успешно добавлен в курс {course.title}")
            else:
                messages.warning(request, "Этот студент уже записан на курс")
        except User.DoesNotExist:
            messages.error(request, f"Пользователь с ID {student_id} не найден")

    return redirect('courses_list')


def remove_student(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        student_id = request.POST.get("student_id")

        try:
            student = User.objects.get(id=student_id)
            course.students.remove(student)
            messages.success(request, "Студент удалён!")
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден!")

    return redirect('courses_list')


