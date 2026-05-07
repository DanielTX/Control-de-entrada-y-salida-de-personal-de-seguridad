from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import HttpResponse
import csv

from .models import Personal, Area, Entrada, Salida, Perfil
from .forms import LoginForm, EntradaForm, SalidaForm, ConsultaForm, PersonalForm, AreaForm
from .decorators import rol_requerido


# ─────────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'control/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    hoy = timezone.localdate()
    entradas_hoy = Entrada.objects.filter(hora_entrada__date=hoy).count()
    salidas_hoy = Salida.objects.filter(hora_salida__date=hoy).count()
    personal_activo = Entrada.objects.filter(salida__isnull=True).count()
    total_personal = Personal.objects.filter(activo=True).count()

    # Últimas 5 entradas
    ultimas_entradas = Entrada.objects.select_related('personal', 'registrado_por').order_by('-hora_entrada')[:5]
    # Últimas 5 salidas
    ultimas_salidas = Salida.objects.select_related(
        'entrada__personal', 'area_destino'
    ).order_by('-hora_salida')[:5]

    context = {
        'entradas_hoy': entradas_hoy,
        'salidas_hoy': salidas_hoy,
        'personal_activo': personal_activo,
        'total_personal': total_personal,
        'ultimas_entradas': ultimas_entradas,
        'ultimas_salidas': ultimas_salidas,
        'hoy': hoy,
    }
    return render(request, 'control/dashboard.html', context)


# ─────────────────────────────────────────────
# REGISTRO DE ENTRADA
# ─────────────────────────────────────────────

@login_required
@rol_requerido('administrador', 'supervisor')
def registrar_entrada(request):
    form = EntradaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            personal = form.cleaned_data['personal']
            observaciones = form.cleaned_data['observaciones']
            entrada = Entrada.objects.create(
                personal=personal,
                registrado_por=request.user,
                observaciones=observaciones,
            )
            messages.success(
                request,
                f'Entrada registrada para {personal.nombre_completo()} a las '
                f'{timezone.localtime(entrada.hora_entrada).strftime("%H:%M")}.'
            )
            return redirect('dashboard')
    return render(request, 'control/registrar_entrada.html', {'form': form})


# ─────────────────────────────────────────────
# REGISTRO DE SALIDA
# ─────────────────────────────────────────────

@login_required
@rol_requerido('administrador', 'supervisor')
def registrar_salida(request):
    form = SalidaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            entrada = form.cleaned_data['entrada']
            # Verificar que no tenga salida ya registrada
            if hasattr(entrada, 'salida'):
                messages.error(request, 'Este personal ya tiene una salida registrada.')
                return redirect('registrar_salida')
            salida = Salida.objects.create(
                entrada=entrada,
                motivo=form.cleaned_data['motivo'],
                area_destino=form.cleaned_data['area_destino'],
                observaciones=form.cleaned_data['observaciones'],
                registrado_por=request.user,
            )
            messages.success(
                request,
                f'Salida registrada para {entrada.personal.nombre_completo()} a las '
                f'{timezone.localtime(salida.hora_salida).strftime("%H:%M")}.'
            )
            return redirect('dashboard')
    return render(request, 'control/registrar_salida.html', {'form': form})


# ─────────────────────────────────────────────
# CONSULTA DE REGISTROS
# ─────────────────────────────────────────────

@login_required
def consulta_registros(request):
    form = ConsultaForm(request.GET or None)
    registros = Entrada.objects.select_related(
        'personal', 'registrado_por', 'salida', 'salida__area_destino'
    ).order_by('-hora_entrada')

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        nombre = form.cleaned_data.get('nombre')
        motivo = form.cleaned_data.get('motivo')
        area = form.cleaned_data.get('area')

        if fecha_inicio:
            registros = registros.filter(hora_entrada__date__gte=fecha_inicio)
        if fecha_fin:
            registros = registros.filter(hora_entrada__date__lte=fecha_fin)
        if nombre:
            registros = registros.filter(
                Q(personal__nombre__icontains=nombre) |
                Q(personal__apellido__icontains=nombre)
            )
        if motivo:
            registros = registros.filter(salida__motivo=motivo)
        if area:
            registros = registros.filter(salida__area_destino=area)

    return render(request, 'control/consulta.html', {
        'form': form,
        'registros': registros[:200],
    })


# ─────────────────────────────────────────────
# REPORTE DE MOVIMIENTOS (exportar CSV)
# ─────────────────────────────────────────────

@login_required
@rol_requerido('administrador', 'supervisor')
def reporte_movimientos(request):
    form = ConsultaForm(request.GET or None)
    registros = Entrada.objects.select_related(
        'personal', 'registrado_por', 'salida', 'salida__area_destino'
    ).order_by('-hora_entrada')

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        nombre = form.cleaned_data.get('nombre')
        motivo = form.cleaned_data.get('motivo')
        area = form.cleaned_data.get('area')

        if fecha_inicio:
            registros = registros.filter(hora_entrada__date__gte=fecha_inicio)
        if fecha_fin:
            registros = registros.filter(hora_entrada__date__lte=fecha_fin)
        if nombre:
            registros = registros.filter(
                Q(personal__nombre__icontains=nombre) |
                Q(personal__apellido__icontains=nombre)
            )
        if motivo:
            registros = registros.filter(salida__motivo=motivo)
        if area:
            registros = registros.filter(salida__area_destino=area)

    # Exportar CSV si se solicita
    if 'exportar' in request.GET:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="reporte_movimientos.csv"'
        response.write('\ufeff')  # BOM para Excel
        writer = csv.writer(response)
        writer.writerow([
            'Nombre', 'Apellido', 'DNI', 'Cargo',
            'Hora Entrada', 'Hora Salida', 'Motivo Salida',
            'Área Destino', 'Registrado por (entrada)', 'Registrado por (salida)'
        ])
        for e in registros:
            salida = getattr(e, 'salida', None)
            writer.writerow([
                e.personal.nombre,
                e.personal.apellido,
                e.personal.dni,
                e.personal.get_cargo_display(),
                timezone.localtime(e.hora_entrada).strftime('%d/%m/%Y %H:%M'),
                timezone.localtime(salida.hora_salida).strftime('%d/%m/%Y %H:%M') if salida else '',
                salida.get_motivo_display() if salida else '',
                salida.area_destino.nombre if salida else '',
                e.registrado_por.get_full_name() or e.registrado_por.username,
                salida.registrado_por.get_full_name() or salida.registrado_por.username if salida else '',
            ])
        return response

    return render(request, 'control/reporte.html', {
        'form': form,
        'registros': registros[:500],
    })


# ─────────────────────────────────────────────
# GESTIÓN DE PERSONAL (solo Administrador)
# ─────────────────────────────────────────────

@login_required
@rol_requerido('administrador')
def lista_personal(request):
    personal = Personal.objects.all().order_by('apellido', 'nombre')
    return render(request, 'control/personal_lista.html', {'personal': personal})


@login_required
@rol_requerido('administrador')
def crear_personal(request):
    form = PersonalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Personal registrado correctamente.')
        return redirect('lista_personal')
    return render(request, 'control/personal_form.html', {'form': form, 'titulo': 'Nuevo Personal'})


# ─────────────────────────────────────────────
# GESTIÓN DE ÁREAS (solo Administrador)
# ─────────────────────────────────────────────

@login_required
@rol_requerido('administrador')
def lista_areas(request):
    areas = Area.objects.all().order_by('nombre')
    return render(request, 'control/areas_lista.html', {'areas': areas})


@login_required
@rol_requerido('administrador')
def crear_area(request):
    form = AreaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Área registrada correctamente.')
        return redirect('lista_areas')
    return render(request, 'control/area_form.html', {'form': form, 'titulo': 'Nueva Área'})
