from django.urls import path
from .views import register, confirm, user_list

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm/', confirm, name='confirm'),
    path('list/', user_list, name='user_list'),
]