from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """Extiende el usuario con un rol del sistema."""
    ROL_CHOICES = [
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('consulta', 'Consulta'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='consulta')

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Area(models.Model):
    """Catálogo de áreas o destinos disponibles en la organización."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['nombre']


class Personal(models.Model):
    """Personal de seguridad registrado en el sistema."""
    CARGO_CHOICES = [
        ('agente', 'Agente de Seguridad'),
        ('supervisor', 'Supervisor'),
        ('jefe', 'Jefe de Seguridad'),
    ]
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, verbose_name='DNI')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='agente')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Personal'
        verbose_name_plural = 'Personal'
        ordering = ['apellido', 'nombre']


class Entrada(models.Model):
    """Registro de entrada del personal."""
    personal = models.ForeignKey(Personal, on_delete=models.PROTECT, related_name='entradas')
    hora_entrada = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='entradas_registradas'
    )
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Entrada: {self.personal} - {self.hora_entrada.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['-hora_entrada']


class Salida(models.Model):
    """Registro de salida del personal, vinculado a una entrada."""
    MOTIVO_CHOICES = [
        ('fin_turno', 'Fin de turno'),
        ('permiso', 'Permiso personal'),
        ('comision', 'Comisión de servicio'),
        ('emergencia', 'Emergencia'),
        ('capacitacion', 'Capacitación'),
        ('medico', 'Cita médica'),
        ('otro', 'Otro'),
    ]
    entrada = models.OneToOneField(Entrada, on_delete=models.PROTECT, related_name='salida')
    hora_salida = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    area_destino = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='salidas')
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='salidas_registradas'
    )

    def __str__(self):
        return f"Salida: {self.entrada.personal} - {self.hora_salida.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Salida'
        verbose_name_plural = 'Salidas'
        ordering = ['-hora_salida']
