from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/medico/', views.medico_registro, name='medico_registro'),
    path('registro/paciente/', views.paciente_registro, name='paciente_registro'),
    #path('medico/inicio/', views.medico_home, name='medico_home'),
    #path('paciente/inicio/', views.paciente_home, name='paciente_home'),
    path('citas/agendar/', views.agendar_cita, name='agendar_cita'),
    #path('citas/ver/', views.ver_citas, name='ver_citas'),
    path('paciente/citas/', views.citas_paciente, name='citas_paciente'),
    path('medico/citas/', views.citas_medico, name='citas_medico'),
    path('consulta/<int:cita_id>/', views.ver_consulta, name='ver_consulta'),
    path('paciente/cita/<int:cita_id>/',views.detalle_cita_paciente, name='detalle_cita_paciente'),
    path('medico/cita/editar/<int:cita_id>/',views.editar_cita, name='editar_cita'),
    path('medico/cita/eliminar/<int:cita_id>/',views.eliminar_cita, name='eliminar_cita'),
    path('paciente/cita/cancelar/<int:cita_id>/',views.cancelar_cita, name='cancelar_cita'),
    path('paciente/cita/reprogramar/<int:cita_id>/',views.reprogramar_cita, name='reprogramar_cita'),
    path('ajax/medicos_por_especialidad/',views.medicos_por_especialidad, name='medicos_por_especialidad'),
    path('paciente/cita/<int:cita_id>/resultado_pdf/',views.descargar_resultado_pdf, name='descargar_resultado_pdf'),
]
