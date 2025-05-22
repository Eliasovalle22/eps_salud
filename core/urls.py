from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/medico/', views.medico_registro, name='medico_registro'),
    path('registro/paciente/', views.paciente_registro, name='paciente_registro'),
    path('medico/inicio/', views.medico_home, name='medico_home'),
    path('paciente/inicio/', views.paciente_home, name='paciente_home'),
    #pasiente
    
]
