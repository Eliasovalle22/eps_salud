from django import forms
from .models import Medico, Paciente, Cita
from django.contrib.auth.hashers import make_password, check_password


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


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
        }
