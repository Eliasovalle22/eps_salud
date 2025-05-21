from django.contrib import admin
from .models import Unidad, Medico, Paciente, Cita, Consulta
# Register your models here.


admin.site.register(Unidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Consulta)
