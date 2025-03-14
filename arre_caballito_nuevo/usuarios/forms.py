from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UsuarioCreationForm(UserCreationForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES_CHOICES, initial='Sin rol')

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('rol',)

class UsuarioChangeForm(UserChangeForm):
    rol = forms.ChoiceField(choices=Usuario.ROLES_CHOICES)

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = UserChangeForm.Meta.fields + ('rol',)