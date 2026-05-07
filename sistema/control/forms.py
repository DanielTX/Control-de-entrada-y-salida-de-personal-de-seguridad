from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Personal, Entrada, Salida, Area


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )


class EntradaForm(forms.Form):
    """Formulario para registrar la entrada de un personal."""
    personal = forms.ModelChoiceField(
        queryset=Personal.objects.filter(activo=True).order_by('apellido', 'nombre'),
        label='Personal',
        empty_label='-- Seleccione personal --',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class SalidaForm(forms.Form):
    """Formulario para registrar la salida de un personal."""
    entrada = forms.ModelChoiceField(
        queryset=Entrada.objects.filter(salida__isnull=True).select_related('personal').order_by('-hora_entrada'),
        label='Personal (entrada activa)',
        empty_label='-- Seleccione entrada activa --',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    motivo = forms.ChoiceField(
        choices=Salida.MOTIVO_CHOICES,
        label='Motivo de salida',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area_destino = forms.ModelChoiceField(
        queryset=Area.objects.filter(activa=True).order_by('nombre'),
        label='Área de destino',
        empty_label='-- Seleccione área --',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    observaciones = forms.CharField(
        label='Observaciones',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class ConsultaForm(forms.Form):
    """Formulario de filtros para consultar registros."""
    fecha_inicio = forms.DateField(
        label='Fecha inicio',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    fecha_fin = forms.DateField(
        label='Fecha fin',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    nombre = forms.CharField(
        label='Nombre o apellido',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por nombre...'})
    )
    motivo = forms.ChoiceField(
        choices=[('', 'Todos los motivos')] + list(Salida.MOTIVO_CHOICES),
        label='Motivo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area = forms.ModelChoiceField(
        queryset=Area.objects.filter(activa=True).order_by('nombre'),
        label='Área',
        required=False,
        empty_label='Todas las áreas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['nombre', 'apellido', 'dni', 'cargo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
