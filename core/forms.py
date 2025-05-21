from django import forms
from .models import Medico, Paciente


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class MedicoRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Medico
        fields = ['nombre', 'especialidad', 'jornada','username', 'password', 'unidad']


class PacienteRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Paciente
        fields = ['identificacion', 'nombre', 'edad','tipo_afiliacion', 'username', 'password', 'unidad']
