from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Medico, Paciente, Cita
from .forms import LoginForm, MedicoRegistroForm, PacienteRegistroForm, CitaForm
from django.http import HttpResponse
from datetime import date

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


# -------------------VISTA AGENDAR CITA-------------------------
def agendar_cita(request):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')

    paciente_id = request.session.get('user_id')
    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            medico = cita.medico
            fecha = cita.fecha

            # Validar disponibilidad
            citas_en_dia = Cita.objects.filter(
                medico=medico, fecha=fecha).count()
            if citas_en_dia >= 10:
                messages.error(
                    request, 'El médico ya tiene 10 citas para ese día.')
            else:
                cita.paciente = paciente
                cita.unidad = medico.unidad
                cita.estado = 'P'
                cita.save()
                messages.success(request, 'Cita agendada correctamente.')
                return redirect('paciente_home')
    else:
        form = CitaForm()

    return render(request, 'core/agendar_cita.html', {'form': form})
def ver_citas(request):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')

    paciente_id = request.session.get('user_id')
    paciente = Paciente.objects.get(id=paciente_id)
    citas = Cita.objects.filter(paciente=paciente)

    return render(request, 'core/ver_citas.html', {'citas': citas})



# -------------------VISTA CITAS PACIENTE-------------------------
def citas_paciente(request):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')

    paciente_id = request.session.get('user_id')
    citas = Cita.objects.filter(
        paciente__id=paciente_id).order_by('-fecha', '-hora')

    return render(request, 'core/citas_paciente.html', {'citas': citas})

# -------------------VISTA CITAS MEDICO-------------------------
def citas_medico(request):
    if request.session.get('user_type') != 'medico':
        return redirect('login')

    medico_id = request.session.get('user_id')
    hoy = date.today()

    citas = Cita.objects.filter(
        medico__id=medico_id,
        fecha=hoy
    ).order_by('hora')

    return render(request, 'core/citas_medico.html', {'citas': citas, 'hoy': hoy})
