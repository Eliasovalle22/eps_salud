from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Medico, Paciente
from .forms import LoginForm, MedicoRegistroForm, PacienteRegistroForm

# Create your views here.

#-------------------VISTA LOGIN-------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            

            medico = Medico.objects.filter(username=username).first()
            if medico and check_password(password, medico.password):
                request.session['user_id'] = medico.id
                request.session['user_type'] = 'medico'
                return redirect('medico_home')

            paciente = Paciente.objects.filter(username=username).first()
            if paciente and check_password(password, paciente.password):
                request.session['user_id'] = paciente.id
                request.session['user_type'] = 'paciente'
                return redirect('paciente_home')

            messages.error(request, 'Credenciales incorrectas')

    else:
        form = LoginForm()
    
    return render(request, 'core/login.html', {'form': form})


# -------------------VISTA REGISTRO MEDICO-------------------------
def medico_registro(request):
    if request.method == 'POST':
        form = MedicoRegistroForm(request.POST)
        if form.is_valid():
            medico = form.save(commit=False)
            medico.password = make_password(form.cleaned_data['password'])
            medico.save()
            messages.success(request, 'Registro exitoso. Inicie sesión.')
            return redirect('login')
    else:
        form = MedicoRegistroForm()
    return render(request, 'core/medico_registro.html', {'form': form})


# -------------------VISTA REGISTRO PACIENTE-------------------------
def paciente_registro(request):
    if request.method == 'POST':
        form = PacienteRegistroForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.password = make_password(form.cleaned_data['password'])
            paciente.save()
            messages.success(request, 'Registro exitoso. Inicie sesión.')
            return redirect('login')
    else:
        form = PacienteRegistroForm()
    return render(request, 'core/paciente_registro.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')

# -------------------VISTA MEDICO HOME-------------------------


def medico_home(request):
    if request.session.get('user_type') != 'medico':
        return redirect('login')
    return render(request, 'core/medico_home.html')


# -------------------VISTA PACIENTE HOME-------------------------
def paciente_home(request):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')
    return render(request, 'core/paciente_home.html')

