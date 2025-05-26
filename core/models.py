from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.


class Unidad(models.Model):
    nombre = models.CharField(max_length=100)
    planta = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unidades'
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nombre
    
    
class Medico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Fractura', 'Fractura'),
        ('General', 'General'),
        ('Internista', 'Internista'),
        ('Dermatólogo', 'Dermatólogo'),
        ('Pediatría', 'Pediatría'),
    ]
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    jornada = models.CharField(max_length=50, choices=[('M', 'Matinal'), ('V', 'Vespertina')])
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    unidad = models.OneToOneField(Unidad, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medicos'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
        
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Solo hashea si no está hasheada ya
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    

class Paciente(models.Model):
    tipo_afiliacion_choices = [
        ('contributivo', 'Contributivo'),
        ('subsidiado', 'Subsidiado'),
    ]
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    tipo_afiliacion = models.CharField(max_length=50, choices=tipo_afiliacion_choices)
    fecha_ingreso = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pacientes'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    
class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=50, choices=[('P', 'Pendiente'), ('C', 'Confirmada'), ('A', 'Anulada')])
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'citas'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        
    def __str__(self):
        return f"Cita de {self.paciente.nombre} con {self.medico.nombre} el {self.fecha} a las {self.hora}"
    

class Consulta(models.Model):
    cita = models.OneToOneField('Cita', on_delete=models.CASCADE, related_name='consulta')
    sintoma = models.TextField()
    tratamiento = models.TextField()
    fecha_atencion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'consultas'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        
    def __str__(self):
        return f"Consulta de {self.cita.paciente.nombre} con {self.cita.medico.nombre} el {self.cita.fecha} a las {self.cita.hora}"