
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = get_user_model()  # Esto usará tu modelo `Usuario` personalizado
        fields = ['username', 'password']
