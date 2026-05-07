"""
Comando para cargar datos iniciales del sistema:
- Áreas predefinidas
- Superusuario administrador
- Usuarios de prueba con cada rol
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from control.models import Area, Personal, Perfil


AREAS = [
    ('Recepción Principal', 'Área de recepción y bienvenida'),
    ('Sala de Operaciones', 'Centro de operaciones de seguridad'),
    ('Almacén', 'Área de almacenamiento y logística'),
    ('Oficinas Administrativas', 'Piso de oficinas administrativas'),
    ('Estacionamiento', 'Área de estacionamiento vehicular'),
    ('Comedor', 'Área de comedor y descanso'),
    ('Sala de Reuniones', 'Salas de conferencias y reuniones'),
    ('Planta de Producción', 'Área de producción industrial'),
    ('Laboratorio', 'Área de laboratorio e investigación'),
    ('Exterior / Patrullaje', 'Rondas externas y perímetro'),
]

PERSONAL_DEMO = [
    ('Juan', 'García López', '12345678', 'agente'),
    ('María', 'Rodríguez Pérez', '87654321', 'supervisor'),
    ('Carlos', 'Mendoza Torres', '11223344', 'agente'),
    ('Ana', 'Flores Quispe', '44332211', 'jefe'),
    ('Luis', 'Vargas Huanca', '55667788', 'agente'),
]


class Command(BaseCommand):
    help = 'Carga datos iniciales: áreas, personal de prueba y usuarios del sistema'

    def handle(self, *args, **options):
        self.stdout.write('Cargando áreas...')
        for nombre, desc in AREAS:
            area, created = Area.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
            if created:
                self.stdout.write(f'  + Área creada: {nombre}')

        self.stdout.write('Cargando personal de prueba...')
        for nombre, apellido, dni, cargo in PERSONAL_DEMO:
            p, created = Personal.objects.get_or_create(
                dni=dni,
                defaults={'nombre': nombre, 'apellido': apellido, 'cargo': cargo}
            )
            if created:
                self.stdout.write(f'  + Personal: {apellido}, {nombre}')

        self.stdout.write('Creando usuarios del sistema...')

        # Superusuario / Administrador
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin', password='admin123',
                first_name='Administrador', last_name='Sistema',
                email='admin@sistema.com'
            )
            Perfil.objects.create(usuario=admin, rol='administrador')
            self.stdout.write('  + admin / admin123  (Administrador)')

        # Supervisor
        if not User.objects.filter(username='supervisor').exists():
            sup = User.objects.create_user(
                username='supervisor', password='super123',
                first_name='Carlos', last_name='Supervisor'
            )
            Perfil.objects.create(usuario=sup, rol='supervisor')
            self.stdout.write('  + supervisor / super123  (Supervisor)')

        # Consulta
        if not User.objects.filter(username='consulta').exists():
            con = User.objects.create_user(
                username='consulta', password='consulta123',
                first_name='Ana', last_name='Consulta'
            )
            Perfil.objects.create(usuario=con, rol='consulta')
            self.stdout.write('  + consulta / consulta123  (Consulta)')

        self.stdout.write(self.style.SUCCESS('\n✓ Datos iniciales cargados correctamente.'))
        self.stdout.write('\nUsuarios disponibles:')
        self.stdout.write('  admin       / admin123    → Administrador (acceso total)')
        self.stdout.write('  supervisor  / super123    → Supervisor (entrada/salida/reportes)')
        self.stdout.write('  consulta    / consulta123 → Consulta (solo lectura)')
