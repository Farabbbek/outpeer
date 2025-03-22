from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
import random
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.paginator import Paginator
from courses.models import Course



User = get_user_model() 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.confirmation_code = str(random.randint(100000, 999999))  # Генерируем код подтверждения
            
            user.save()  

          
            email = EmailMessage(
                'Код подтверждения',
                f'Ваш код подтверждения: {user.confirmation_code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.encoding = 'utf-8'
            email.send(fail_silently=False)

            return redirect('confirm')  
    else:
        form = RegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()  
        print(f"Введённый код: {code}")  
        
        try:
            user = User.objects.get(confirmation_code=code, is_confirmed=False)
            print(f"Найден пользователь: {user.email}, код: {user.confirmation_code}")

            user.is_active = True
            user.is_confirmed = True
            user.confirmation_code = ""
            user.save(update_fields=['is_active', 'is_confirmed', 'confirmation_code'])

            messages.success(request, "Аккаунт подтверждён! Теперь можно войти.")
            return redirect('user_list')
        except User.DoesNotExist:
            messages.error(request, "Неверный код подтверждения или аккаунт уже активирован.")
    
    return render(request, 'users/confirm.html')

def user_list(request):
    users = User.objects.prefetch_related('enrolled_courses').all()
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request, 'users/user_list.html', {'page_obj': page_obj})

def course_list(request):
    courses = Course.objects.all().order_by('name')
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/courses_list.html', {'page_obj': page_obj})
