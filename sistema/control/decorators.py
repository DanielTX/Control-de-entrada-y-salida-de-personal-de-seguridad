from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def rol_requerido(*roles):
    """Decorador que restringe el acceso según el rol del usuario."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            # Superusuario tiene acceso total
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            try:
                rol_usuario = request.user.perfil.rol
            except Exception:
                messages.error(request, 'Su cuenta no tiene un perfil asignado. Contacte al administrador.')
                return redirect('dashboard')
            if rol_usuario in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'No tiene permisos para acceder a esta sección.')
            return redirect('dashboard')
        return _wrapped_view
    return decorator
