from django import forms
from .models import Medico, Paciente, Cita,Consulta
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
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'jornada': forms.Select(attrs={'class': 'form-select'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-select'}),
        }


class PacienteRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Paciente
        fields = ['identificacion', 'nombre', 'edad','tipo_afiliacion', 'username', 'password', 'unidad']
        widgets = {
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_afiliacion': forms.Select(attrs={'class': 'form-select'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-select'}),
        }


class CitaForm(forms.ModelForm):
    especialidad = forms.ChoiceField(
        choices=Medico.ESPECIALIDAD_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Cita
        fields = ['especialidad', 'medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicialmente, muestra todos los médicos
        self.fields['medico'].queryset = Medico.objects.all()
        # Si ya se seleccionó una especialidad, filtra los médicos
        if 'especialidad' in self.data:
            especialidad = self.data.get('especialidad')
            if especialidad:
                self.fields['medico'].queryset = Medico.objects.filter(
                    especialidad=especialidad)


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['sintoma', 'tratamiento']
        widgets = {
            'sintoma': forms.Textarea(attrs={'class': 'form-control'}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control'}),
        }
