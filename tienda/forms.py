from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Usuario

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'direccion', 'teléfono', 'RFC', 'password1', 'password2']

class CustomUserAuthenticationForm(AuthenticationForm):
    pass
