from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/medico/', views.medico_registro, name='medico_registro'),
    path('registro/paciente/', views.paciente_registro, name='paciente_registro'),
    path('medico/inicio/', views.medico_home, name='medico_home'),
    path('paciente/inicio/', views.paciente_home, name='paciente_home'),
    path('citas/agendar/', views.agendar_cita, name='agendar_cita'),
    path('citas/ver/', views.ver_citas, name='ver_citas'),
    path('paciente/citas/', views.citas_paciente, name='citas_paciente'),
    path('medico/citas/', views.citas_medico, name='citas_medico'),

]
