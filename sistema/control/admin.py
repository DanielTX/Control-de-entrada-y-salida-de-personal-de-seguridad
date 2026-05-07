from django.contrib import admin
from .models import Perfil, Area, Personal, Entrada, Salida


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    list_filter = ('rol',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'dni', 'cargo', 'activo')
    list_filter = ('cargo', 'activo')
    search_fields = ('nombre', 'apellido', 'dni')


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('personal', 'hora_entrada', 'registrado_por')
    list_filter = ('hora_entrada',)
    search_fields = ('personal__nombre', 'personal__apellido')
    readonly_fields = ('hora_entrada', 'registrado_por')


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ('entrada', 'hora_salida', 'motivo', 'area_destino', 'registrado_por')
    list_filter = ('motivo', 'hora_salida', 'area_destino')
    search_fields = ('entrada__personal__nombre', 'entrada__personal__apellido')
    readonly_fields = ('hora_salida', 'registrado_por')
