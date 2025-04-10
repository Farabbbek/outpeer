from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User 
 
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2', 'role')