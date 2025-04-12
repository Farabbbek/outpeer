from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson
from .serializers import LessonSerializer
from courses.models import Course
from courses.serializers import CourseSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt


def create_lesson_html(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        material_url = request.POST.get('material_url')

        Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            material_url=material_url or ''
        )
        return redirect('lessons-by-course', course_id=course.id)

    return redirect('lessons-by-course', course_id=course.id)


def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        material_url = request.POST.get('material_url')

        Lesson.objects.create(
            course=course,
            title=title,
            content=content,
            material_url=material_url or ''
        )
        return redirect('lessons_list')

    return render(request, 'lessons/add_lesson.html', {'course': course})


def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('lessons_list')


@api_view(['GET'])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def lessons_by_course(request, course_id):
    lessons = Lesson.objects.filter(course_id=course_id)
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def lesson_detail(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)


@api_view(['POST'])
def create_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LessonSerializer(lesson, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@csrf_exempt
def delete_lesson_api(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    lesson.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def lessons_html_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'lessons/lesson_list.html', {
        'course': course,
        'lessons': lessons
    })


def all_lessons_view(request):
    course_id = request.GET.get('course_id')
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        lessons = Lesson.objects.filter(course=course).select_related('course')
    else:
        course = Course.objects.first()
        lessons = Lesson.objects.select_related('course').all() if not course else Lesson.objects.filter(course=course).select_related('course')

    return render(request, 'lessons/all_lessons.html', {
        'course': course,
        'lessons': lessons
    })