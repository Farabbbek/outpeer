from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class User(AbstractUser):
    ROLES = [
        ('student', 'Student'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),  
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='student')
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email  
        
    def generate_confirmation_code(self):
        self.confirmation_code = str(random.randint(100000, 999999))
        self.save()
