from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Medico, Paciente, Cita
from .forms import LoginForm, MedicoRegistroForm, PacienteRegistroForm, CitaForm, ConsultaForm
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
                return redirect('citas_medico')

            paciente = Paciente.objects.filter(username=username).first()
            if paciente and check_password(password, paciente.password):
                request.session['user_id'] = paciente.id
                request.session['user_type'] = 'paciente'
                return redirect('citas_paciente')

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


# def citas_medico(request):
#     if request.session.get('user_type') != 'medico':
#         return redirect('login')

#     medico_id = request.session.get('user_id')
#     medico = Medico.objects.get(id=medico_id)
#     citas = Cita.objects.filter(
#         medico__id=medico_id
#     ).order_by('-fecha', 'hora')

#     return render(request, 'core/citas_medico.html', {
#         'citas': citas,
#         'medico': medico,
#     })


# -------------------VISTA PACIENTE HOME-------------------------
# def citas_paciente(request):
#     if request.session.get('user_type') != 'paciente':
#         return redirect('login')

#     paciente_id = request.session.get('user_id')
#     paciente = Paciente.objects.get(id=paciente_id)
#     citas = Cita.objects.filter(paciente=paciente)

#     return render(request, 'core/citas_paciente.html', {'citas': citas})


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
                return redirect('citas_paciente')
    else:
        form = CitaForm()

    return render(request, 'core/agendar_cita.html', {'form': form})

# -------------------VISTA VER CITAS-------------------------
# def ver_citas(request):
#     if request.session.get('user_type') != 'paciente':
#         return redirect('login')

#     paciente_id = request.session.get('user_id')
#     paciente = Paciente.objects.get(id=paciente_id)
#     citas = Cita.objects.filter(paciente=paciente)

#     return render(request, 'core/ver_citas.html', {'citas': citas})


# -------------------VISTA VER CONSULTAS-------------------------
def ver_consulta(request, cita_id):
    if request.session.get('user_type') != 'medico':
        return redirect('login')
    cita = get_object_or_404(Cita, id=cita_id)
    consulta = getattr(cita, 'consulta', None)

    if consulta:
        # Solo permite cambiar el estado si ya existe consulta
        if request.method == 'POST':
            nuevo_estado = request.POST.get('estado')
            if nuevo_estado in dict(Cita._meta.get_field('estado').choices):
                cita.estado = nuevo_estado
                cita.save()
                messages.success(
                    request, 'Estado de la cita actualizado correctamente.')
                return redirect('ver_consulta', cita_id=cita.id)
        return render(request, 'core/ver_consulta.html', {'cita': cita, 'consulta': consulta})
    else:
        # Permite crear la consulta
        if request.method == 'POST':
            form = ConsultaForm(request.POST)
            if form.is_valid():
                nueva_consulta = form.save(commit=False)
                nueva_consulta.cita = cita
                nueva_consulta.unidad = cita.unidad
                nueva_consulta.save()
                cita.estado = 'C'  # Cambia el estado a Confirmada al crear consulta
                cita.save()
                messages.success(request, 'Consulta registrada correctamente.')
                return redirect('ver_consulta', cita_id=cita.id)
        else:
            form = ConsultaForm()
        return render(request, 'core/crear_consulta.html', {'cita': cita, 'form': form})



# -------------------VISTA CITAS PACIENTE-------------------------
def citas_paciente(request):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')

    paciente_id = request.session.get('user_id')
    paciente = Paciente.objects.get(id=paciente_id)
    citas = Cita.objects.filter(
        paciente__id=paciente_id).order_by('-fecha', '-hora')

    return render(request, 'core/citas_paciente.html', {
        'citas': citas,
        'paciente': paciente,
    })


# -------------------VISTA CITAS MEDICO-------------------------
def citas_medico(request):
    if request.session.get('user_type') != 'medico':
        return redirect('login')

    medico_id = request.session.get('user_id')
    medico = Medico.objects.get(id=medico_id)
    citas = Cita.objects.filter(
        medico__id=medico_id
    ).order_by('-fecha', 'hora')

    return render(request, 'core/citas_medico.html', {
        'citas': citas,
        'medico': medico,
    })


#--------------------DETALLE CITA PACIENTE-------------------------
def detalle_cita_paciente(request, cita_id):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')

    cita = get_object_or_404(Cita, id=cita_id, paciente__id=request.session.get('user_id'))
    consulta = getattr(cita, 'consulta', None)

    return render(request, 'core/detalle_cita_paciente.html', {'cita': cita, 'consulta': consulta})

#--------------------EDITAR CITA-------------------------
def editar_cita(request, cita_id):
    if request.session.get('user_type') != 'medico':
        return redirect('login')
    cita = get_object_or_404(
        Cita, id=cita_id, medico_id=request.session.get('user_id'))
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita modificada correctamente.')
            return redirect('citas_medico')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'core/editar_cita.html', {'form': form, 'cita': cita})

#--------------------ELIMINAR CITA-------------------------
def eliminar_cita(request, cita_id):
    if request.session.get('user_type') != 'medico':
        return redirect('login')
    cita = get_object_or_404(
        Cita, id=cita_id, medico_id=request.session.get('user_id'))
    if request.method == 'POST':
        cita.delete()
        messages.success(request, 'Cita eliminada correctamente.')
        return redirect('citas_medico')
    return render(request, 'core/eliminar_cita.html', {'cita': cita})

#--------------------CANCELAR CITA-------------------------
def cancelar_cita(request, cita_id):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')
    cita = get_object_or_404(
        Cita, id=cita_id, paciente_id=request.session.get('user_id'))
    if request.method == 'POST':
        cita.estado = 'A'  # Anulada
        cita.save()
        messages.success(request, 'Cita cancelada correctamente.')
        return redirect('citas_paciente')
    return render(request, 'core/cancelar_cita.html', {'cita': cita})

#--------------------REPROGRAMAR CITA-------------------------
def reprogramar_cita(request, cita_id):
    if request.session.get('user_type') != 'paciente':
        return redirect('login')
    cita = get_object_or_404(
        Cita, id=cita_id, paciente_id=request.session.get('user_id'), estado='P')
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita reprogramada correctamente.')
            return redirect('citas_paciente')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'core/reprogramar_cita.html', {'form': form, 'cita': cita})
